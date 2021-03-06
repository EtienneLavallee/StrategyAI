# Under MIT license, see LICENSE.txt

from Util.pose import Pose

from Util.position import Position
from Util.role import Role
from Util.role_mapping_rule import keep_prev_mapping_otherwise_random
from ai.STA.Strategy.strategy import Strategy
from ai.STA.Tactic.go_kick import GoKick
from ai.states.game_state import GameState


class OffenseKickOff(Strategy):
    def __init__(self, p_game_state):
        super().__init__(p_game_state)

        middle_player = self.assigned_roles[Role.MIDDLE]

        self.create_node(Role.MIDDLE, GoKick(self.game_state, middle_player, self.game_state.field.their_goal_pose))

    @classmethod
    def required_roles(cls):
        return {Role.MIDDLE: keep_prev_mapping_otherwise_random}
