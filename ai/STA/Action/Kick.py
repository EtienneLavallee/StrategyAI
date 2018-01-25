# Under MIT license, see LICENSE.txt

from RULEngine.GameDomainObjects.player import Player
from Util.ai_command_shit import AICommand, AICommandType
from Util.Pose import Pose
from ai.STA.Action.Action import Action
from ai.states.game_state import GameState


class Kick(Action):

    def __init__(self, game_state: GameState, player: Player, force: [int, float], target: Pose=Pose(), end_speed=0,
                 cruise_speed=0.1):
        """
            :param game_state: Current state of the game
            :param player: Instance of the player
            :param p_force: Kick force [0, 10]
        """
        # TODO check the force not used by the new interface! MGL 2017/05/23
        Action.__init__(self, game_state, player)
        assert(isinstance(force, (int, float)))
        self.force = force
        self.target = target
        self.end_speed = end_speed

    def exec(self):
        """
        Execute the kick command
        :return: Un AIcommand
        """
        if self.target is not None:
            ball_position = self.game_state.get_ball_position()
            orientation = (self.target.position - self.player.pose.position).angle()
        else:
            ball_position = self.player.pose.position
            orientation = self.player.pose.orientation

        cmd_params = {"pose_goal": Pose(ball_position, orientation),
                      "kick": True,
                      "pathfinder_on": True,
                      "kick_strength": self.force,
                      "cruise_speed": 0.1,
                      "charge_kick": True,
                      "end_speed":self.end_speed}

        return AICommand(self.player, AICommandType.MOVE, **cmd_params)
