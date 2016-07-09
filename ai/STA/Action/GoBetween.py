# Under MIT licence, see LICENCE.txt
from math import sqrt
from .Action import Action
from ...Util.types import AICommand
from ...Util.geometry import distance
from RULEngine.Util.Pose import Pose
from RULEngine.Util.Position import Position
from RULEngine.Util.area import stayOutsideCircle
from RULEngine.Util.geometry import get_angle

__author__ = 'Robocup ULaval'


class GoBetween(Action):
    """
    Action GoBetween: D�place le robot au point le plus proche sur la droite entre deux positions pass�es en param�tres
    M�thodes :
        exec(self): Retourne la pose o� se rendre
    Attributs (en plus de ceux de Action):
        player_id : L'identifiant du joueur
        position1 : La premi�re position formant la droite
        position2 : La deuxi�me position formant la droite
        minimum_distance : La distance minimale qu'il doit y avoir entre le robot et chacun des points
    """
    def __init__(self, p_info_manager, p_player_id, p_position1, p_position2, p_minimum_distance=0):
        """
            :param p_info_manager: r�f�rence vers l'InfoManager
            :param p_player_id: Identifiant du joueur qui doit se d�placer
            :param p_position1: La premi�re position formant la droite
            :param p_position2: La deuxi�me position formant la droite
            :param p_minimum_distance: La distance minimale qu'il doit y avoir entre le robot et chacun des points
        """
        Action.__init__(self, p_info_manager)
        assert(isinstance(p_player_id, int))
        assert(isinstance(p_position1, Position))
        assert(isinstance(p_position2, Position))
        assert(isinstance(p_minimum_distance, (int, float)))
        assert(distance(p_position1, p_position2) > 2*p_minimum_distance)

        self.player_id = p_player_id
        self.position1 = p_position1
        self.position2 = p_position2
        self.minimum_distance = p_minimum_distance

    def exec(self):
        """
        Calcul le point le plus proche du robot sur la droite entre les deux positions
        :return: Un tuple (Pose, kick) o� Pose est la destination du joueur et kick est nul (on ne botte pas)
        """
        robot_position = self.info_manager.get_player_pose(self.player_id).position
        delta_x = self.position2.x - self.position1.x
        delta_y = self.position2.y - self.position1.y

        # �quation de la droite reliant les deux positions
        a1 = delta_y / delta_x                                  # pente
        b1 = self.position1.y - a1*self.position1.x             # ordonn�e � l'origine

        # �quation de la droite perpendiculaire
        a2 = -1/a1                                              # pente perpendiculaire � a1
        b2 = robot_position.y - a2*robot_position.x             # ordonn�e � l'origine

        # Calcul des coordonn�es de la destination
        x = (b2 - b1)/(a1 - a2)                                 # a1*x + b1 = a2*x + b2
        y = a1*x + b1
        destination_position = Position(x, y)

        # V�rification que destination_position se trouve entre position1 et position2
        distance_positions = sqrt(delta_x**2 + delta_y**2)
        distance_dest_pos1 = distance(self.position1, destination_position)
        distance_dest_pos2 = distance(self.position2, destination_position)

        if distance_dest_pos1 >= distance_positions: # Si position2 est entre position1 et destination_position
            new_x = self.position2.x - self.minimum_distance * delta_x / distance_positions
            new_y = self.position2.y - self.minimum_distance * delta_y / distance_positions
            destination_position = Position(new_x, new_y)
        elif distance_dest_pos2 >= distance_positions: # Si position1 est entre position2 et destination_position
            new_x = self.position1.x + self.minimum_distance * delta_x / distance_positions
            new_y = self.position1.y + self.minimum_distance * delta_y / distance_positions
            destination_position = Position(new_x, new_y)

        # V�rification que destination_position respecte la distance minimale
        if distance_dest_pos1 <= distance_dest_pos2:
            destination_position = stayOutsideCircle(destination_position, self.position1, self.minimum_distance)
        else:
            destination_position = stayOutsideCircle(destination_position, self.position2, self.minimum_distance)

        # Calcul de l'orientation de la pose de destination
        destination_orientation = get_angle(destination_position, self.info_manager.get_player_target)
        # TODO: v�rifier l'utilisation de target vs goal

        destination_pose = Pose(destination_position, destination_orientation)
        kick_strength = 0
        return AICommand(destination_pose, kick_strength)
