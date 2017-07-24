# Under MIT License, see LICENSE.txt

import numpy as np
import warnings
from profilehooks import profile

class Position(np.ndarray):

    def __new__(cls, *args, z=0, abs_tol=0.01):
        obj = position_builder(args, cls)
        obj.x = obj[0]
        obj.y = obj[1]
        obj.z = z
        obj._abs_tol = abs_tol

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.z = 0
        self._abs_tol = 0.01

    @property
    def x(self):
        return float(self[0])

    @x.setter
    def x(self, x):
        self[0] = x

    @property
    def y(self):
        return float(self[1])

    @y.setter
    def y(self, y):
        self[1] = y

    @property
    def abs_tol(self):
        return getattr(self, '_abs_tol', 0.01)

    @abs_tol.setter
    def abs_tol(self, abs_tol):
        self._abs_tol = abs_tol


    def norm(self):
        """Return the distance of the point from the origin"""

        return np.sqrt(self[0] ** 2 + self[1] ** 2)
        # return np.sqrt(np.dot(np.array([self[0], self[1]]), np.array([self[0], self[1]])))
        #return float(np.linalg.norm(self.view(np.ndarray)))

    def angle(self):
        """Return the angle of the point from the x-axis between -pi and pi"""
        if self == Position(0, 0):
            warnings.warn('Angle is not defined for (0, 0). Result will be 0.')
        return float(np.arctan2(self[1], self[0]))

    def rotate(self, angle):
        rotation = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]).view(Position)
        return np.dot(rotation, self)

    def normalized(self):
        if self.norm() == 0:
            raise ZeroDivisionError
        return self / self.norm()

    def perpendicular(self):
        """Retourne la normal unitaire entre le vecteur et la normal au plan np.array([0,0,1])"""
        normalized_pose = self.normalized()
        array_temp = np.array([normalized_pose[0], normalized_pose[1], 0])
        z_vector = np.array([0, 0, 1])
        res = np.cross(array_temp, z_vector)
        return Position(res[0], res[1])

    def __eq__(self, other):
        if isinstance(other, Position):
            min_abs_tol = min(self.abs_tol, other.abs_tol)
            return np.allclose(self, other, atol=min_abs_tol)
        elif isinstance(other, np.ndarray) and other.size == 2:
            min_abs_tol = self.abs_tol
            return np.allclose(self, other, atol=min_abs_tol)
        else:
            raise TypeError

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_array(self):
        return self

    def conv_2_np(self):
        """Legacy. Do not use."""
        return self.to_array()

    @staticmethod
    def from_np(array):
        """Legacy. Do not use."""
        return Position(array)

    def __repr__(self):
        return 'Position({:8.3f}, {:8.3f})'.format(self[0], self[1])

    def __str__(self):
        return '[{:8.3f}, {:8.3f}]'.format(self[0], self[1])

    def __hash__(self):
        return hash(str(self))

def position_builder(args, cls):

    if len(args) == 0:
        obj = Position(0, 0)
    elif len(args) == 1:
        if len(args[0]) == 2:
            obj = np.asarray(args[0]).view(cls)
        # elif isinstance(args[0], tuple) and len(args[0]) == 2:
        #     obj = np.asarray(args[0]).view(cls)
        else:
            raise ValueError
    elif len(args) == 2:
        obj = np.asarray(args).view(cls)
    else:
        raise ValueError

    return obj
