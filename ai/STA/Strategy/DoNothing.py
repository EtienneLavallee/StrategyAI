# Under MIT License, see LICENSE.txt
from RULEngine.Util.constant import PLAYER_PER_TEAM
from ai.STA.Tactic.Stop import Stop
from ai.Util.role import Role
from . Strategy import Strategy


class DoNothing(Strategy):
    def __init__(self, p_game_state):
        super().__init__(p_game_state)
        for r in Role:
            p = self.game_state.get_player_by_role(r)
            if p is None: continue
            self.add_tactic(r, Stop(self.game_state, p))
