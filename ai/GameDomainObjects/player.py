# Under MIT License, see LICENSE.txt
from typing import Dict

from Util.pathfinder_history import PathfinderHistory
from Util.pose import Pose


class Player:

    def __init__(self, number_id: int, team):
        assert isinstance(number_id, int)
        assert number_id in [x for x in range(0, 13)]

        self._id = number_id
        self._team = team
        self._pose = Pose()
        self._velocity = Pose()
        self.pathfinder_history = PathfinderHistory()
        self.pathfinder_on = True

    def update(self, new_pose: Pose, new_velocity: Pose):
        self.pose = new_pose
        self.velocity = new_velocity

    def has_id(self, pid):
        return self.id == pid

    def __str__(self):
        return str(self.team.team_color.name)+" "+str(self.id)

    @property
    def id(self):
        return self._id

    @property
    def team(self):
        return self._team

    @property
    def pose(self):
        return self._pose

    @pose.setter
    def pose(self, value):
        assert isinstance(value, Pose)
        self._pose = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        assert isinstance(value, Pose)
        self._velocity = value

    @property
    def team_color(self):
        return self.team.team_color

    @classmethod
    def from_dict(cls, dict: Dict, team):
        p = Player(dict["id"], team)
        p.pose = Pose.from_dict(dict["pose"])
        # TODO: Use another type of object specific to speed
        p.velocity = Pose.from_dict(dict["pose"])

        return p
