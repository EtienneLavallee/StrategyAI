# Under MIT licence, see LICENCE.txt
from .Action import Action
from ...Util.types import AICommand
from RULEngine.Util.Pose import Pose
from RULEngine.Util.geometry import get_angle

__author__ = 'Robocup ULaval'


class MoveWithBall(Action):
    """
    Action MoveWithBall: D�place le robot en tenant compte de la possession de la balle
    M�thodes :
        exec(self): Retourne la pose o� se rendre
    Attributs (en plus de ceux de Action):
        player_id : L'identifiant du joueur
        destination : La position o� on souhaite d�placer le robot
    """
    def __init__(self, p_info_manager, p_player_id, p_destination):
        """
            :param p_info_manager: r�f�rence vers l'InfoManager
            :param p_player_id: Identifiant du joueur qui se d�place avec la balle
            :param p_destination: La position o� on souhaite d�placer le robot
        """
        Action.__init__(self, p_info_manager)
        self.player_id = p_player_id
        self.destination = p_destination

    def exec(self):
        """
        Ex�cute le d�placement en tenant compte de la possession de la balle. Le robot se d�place vers la destination,
        mais s'oriente de fa�on � garder la balle sur le dribleur. C'est la responsabilit� de la Tactique de faire les
        corrections de trajectoire n�cessaire.
        :return: Un tuple (Pose, kick) o� Pose est la destination du joueur kick est faux (on ne botte pas)
        """
        #TODO: Am�liorer le comportement en ajoutant l'intervalle d'anle correspondant � la largeur du dribleur
        destination_orientation = get_angle(self.info_manager.get_player_pose(self.player_id).position,
                                            self.info_manager.get_ball_position())
        destination_pose = Pose(self.destination, destination_orientation)
        kick_strength = 0
        return AICommand(destination_pose, kick_strength)
