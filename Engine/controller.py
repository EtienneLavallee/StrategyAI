# Under MIT licence, see LICENCE.txt

import logging
import time
from queue import Queue

import numpy as np
from typing import Dict, List, Any

from Debug.debug_command_factory import DebugCommandFactory

from Engine.filters.path_smoother import path_smoother
from Engine.regulators import VelocityRegulator, PositionRegulator
from Engine.robot import Robot
from Engine.Communication.robot_state import RobotPacket, RobotState

from Util import Pose
from Util.constant import ROBOT_RADIUS
from Util.engine_command import EngineCommand
from Util.geometry import rotate

from config.config import Config
config = Config()


class Controller:

    def __init__(self, ui_send_queue: Queue):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ui_send_queue = ui_send_queue

        self.timestamp = -1
        self.robots = [Robot(robot_id) for robot_id in range(config['ENGINE']['max_robot_id'])]
        for robot in self.robots:
            robot.velocity_regulator = VelocityRegulator()
            robot.position_regulator = PositionRegulator()


    def update(self, track_frame: Dict[str, Any], engine_cmds: List[EngineCommand]):

        self.timestamp = track_frame['timestamp']

        for robot in self.robots:
            robot.is_on_field = False

        for robot in track_frame[config['GAME']['our_color']]:
            self[robot['id']].is_on_field = True
            self[robot['id']].pose = robot['pose']
            self[robot['id']].velocity = robot['velocity']

        for cmd in engine_cmds:
            self[cmd.robot_id].engine_cmd = cmd

    def execute(self) -> RobotState:
        commands = {}

        for robot in self.active_robots:
            robot.path, robot.target_speed = path_smoother(robot.raw_path, robot.cruise_speed, robot.end_speed)

            if robot.distance_to_path_end < ROBOT_RADIUS and robot.end_speed == 0:
                robot.velocity_regulator.reset()
                commands[robot.id] = robot.position_regulator.execute(robot)
            else:
                robot.position_regulator.reset()
                commands[robot.id] = robot.velocity_regulator.execute(robot)

        self.send_debug(commands)

        return self.generate_packet(commands)

    def generate_packet(self, commands: Dict[int, Pose]) -> RobotState:
        packet = RobotState(timestamp=self.timestamp,
                            is_team_yellow=config['GAME']['our_color'] == 'yellow',
                            packet=[])

        for robot_id, cmd in commands.items():
            robot = self[robot_id]
            packet.packet.append(
                RobotPacket(robot_id=robot_id,
                            command=self._put_in_robots_referential(robot, cmd),
                            kick_type=robot.engine_cmd.kick_type,
                            kick_force=robot.engine_cmd.kick_force,
                            charge_kick=robot.engine_cmd.charge_kick,
                            dribbler_state=robot.engine_cmd.dribbler_state))
        return packet

    @staticmethod
    def _put_in_robots_referential(robot: Robot, cmd: Pose) -> Pose:
        if config['GAME']['on_negative_side']:
            cmd.x *= -1
            cmd.orientation *= -1
            cmd.position = rotate(cmd.position, np.pi + robot.orientation)
        else:
            cmd.position = rotate(cmd.position, -robot.orientation)
        return cmd

    def send_debug(self, commands: Dict[int, Pose]):
        if not commands:
            return

        robot_id = 0

        if robot_id not in commands:
            return
        self.ui_send_queue.put_nowait(DebugCommandFactory.plot_point('mm/s',
                                                                     'robot {} cmd speed'.format(robot_id),
                                                                     [time.time()],
                                                                     [commands[robot_id].norm]))

        self.ui_send_queue.put_nowait(DebugCommandFactory.plot_point('mm/s',
                                                                     'robot {} Kalman speed'.format(robot_id),
                                                                     [time.time()],
                                                                     [self[robot_id].velocity.norm]))

    @property
    def active_robots(self) -> List[Robot]:
        return [robot for robot in self.robots if robot.is_active]

    def __getitem__(self, item: int) -> Robot:
        return self.robots[item]