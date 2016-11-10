# Under MIT license, see LICENSE.txt

from RULEngine.Util.constant import *
from ai.STA.Tactic.GoGetBall import GoGetBall
from ai.STA.Tactic.GoalKeeper import GoalKeeper
from ai.STA.Tactic.CoverZone import CoverZone
from . Strategy import Strategy
from ai.Algorithm.Node import Node


class SimpleDefense(Strategy):
    def __init__(self, p_game_state):
        super().__init__(p_game_state)

        self.add_tactic(0, GoalKeeper(self.game_state, 0))
        self.add_tactic(1, GoGetBall(self.game_state, 1))
        self.add_tactic(2, CoverZone(self.game_state, 2, FIELD_Y_TOP, 0, FIELD_X_LEFT, FIELD_X_LEFT / 2))
        self.add_tactic(3, CoverZone(self.game_state, 3, 0, FIELD_Y_BOTTOM, FIELD_X_LEFT, FIELD_X_LEFT / 2))
        self.add_tactic(4, CoverZone(self.game_state, 4, FIELD_Y_TOP, 0, FIELD_X_LEFT / 2, 0))
        self.add_tactic(5, CoverZone(self.game_state, 5, 0, FIELD_Y_BOTTOM, FIELD_X_LEFT / 2, 0))
