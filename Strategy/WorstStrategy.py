from Command import Command
from Strategy.Strategy import Strategy
from Util.Position import Position


class WorstStrategy(Strategy):
    def __init__(self, field, referee, team, opponent_team):
        super().__init__(field, referee, team, opponent_team)


    def on_start(self):
        pass

    def on_halt(self):
        pass

    def on_stop(self):
        pass
