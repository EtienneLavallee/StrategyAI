# Under MIT license, see LICENSE.txt
from functools import partial

from RULEngine.Util.Pose import Pose
from RULEngine.Util.Position import Position
from ai.STA.Tactic.go_to_random_pose_in_zone import GoToRandomPosition
from ai.Util.role import Role
from ai.states.game_state import GameState
from . Strategy import Strategy



class Pathfinder_Benchmark(Strategy):
    def __init__(self, p_game_state):
        super().__init__(p_game_state)

        roles_to_consider = [Role.FIRST_ATTACK, Role.SECOND_ATTACK, Role.MIDDLE,
                             Role.FIRST_DEFENCE, Role.SECOND_DEFENCE, Role.GOALKEEPER]
        role_by_robots = [(i, self.game_state.get_player_by_role(i)) for i in roles_to_consider]

        for index, player in role_by_robots:
            if player:
                self.add_tactic(index, GoToRandomPosition(self.game_state, player, Position(1400, 0), 2000, 3000))