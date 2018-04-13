
import logging
from collections import defaultdict
from typing import Dict, List

from Util import AICommand, Position
from ai.Algorithm.path_partitionner import PathPartitionner, PointObstacle, LineObstacle, Obstacle
from ai.GameDomainObjects import Player
from ai.states.game_state import GameState

MIN_DISTANCE_FROM_OBSTACLE = 250


class PathfinderModule:
    def __init__(self):
        self.paths = defaultdict(lambda: None)
        self.logger = logging.getLogger("PathfinderModule")
        self.pathfinder = PathPartitionner()
        self.obstacles = []

    def exec(self, game_state: GameState, ai_cmds: Dict[Player, AICommand]) -> Dict:

        self.updates_obstacles(game_state)

        for player, ai_cmd in ai_cmds.items():
            if ai_cmd.target is not None:
                player_obstacles = self.player_optionnal_obstacles(game_state, ai_cmd)
                self.paths[player] = self.pathfinder.get_path(start=player.position,
                                                              target=ai_cmd.target.position,
                                                              obstacles=player_obstacles,
                                                              last_path=self.paths[player])
            else:
                self.paths[player] = None

        return self.paths

    def updates_obstacles(self, game_state: GameState):

        self.obstacles.clear()

        our_team = [player for player in game_state.our_team.available_players.values()]
        enemy_team = [player for player in game_state.enemy_team.available_players.values()]

        for other in our_team + enemy_team:
            self.obstacles.append(PointObstacle(other.position.array, avoid_distance=MIN_DISTANCE_FROM_OBSTACLE))


    def player_optionnal_obstacles(self, game_state: GameState, ai_cmd: AICommand) -> List[Obstacle]:
        path_obstacles = self.obstacles.copy()

        if ai_cmd.ball_collision and game_state.is_ball_on_field:
            path_obstacles.append(PointObstacle(game_state.ball_position.array, avoid_distance=MIN_DISTANCE_FROM_OBSTACLE))

        if ai_cmd.ball_collision and game_state.is_ball_on_field:
            path_obstacles.append(PointObstacle(game_state.ball_position.array, avoid_distance=MIN_DISTANCE_FROM_OBSTACLE))

        path_obstacles.append(LineObstacle(Position(-3500, 1100).array, Position(-3500, -1100).array, avoid_distance=MIN_DISTANCE_FROM_OBSTACLE))
        path_obstacles.append(LineObstacle(Position(-10000, -1100).array, Position(-3500, -1100).array, avoid_distance=MIN_DISTANCE_FROM_OBSTACLE))
        path_obstacles.append(LineObstacle(Position(-3500, 1100).array, Position(-10000, 1100).array, avoid_distance=MIN_DISTANCE_FROM_OBSTACLE))
        # TODO: add enemy goal
        # self.obstacles.add(LineObstacle(start, end, y_length, avoid_distance=MIN_DISTANCE_FROM_OBSTACLE))

        return path_obstacles
