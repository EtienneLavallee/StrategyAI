# Under MIT License, see LICENSE.txt

from RULEngine.Communication.util.udp_socket import udp_socket
from config.config_service import ConfigService


class UIDebugVisionSender(object):
    """
        Définition du service capable d'envoyer des paquets de débogages au
        serveur et à l'interface de débogage. S'occupe de la sérialisation.
    """
    def __init__(self):
        """ Constructeur """
        cfg = ConfigService()
        host = cfg.config_dict["COMMUNICATION"]["ui_debug_address"]
        port = int(cfg.config_dict["COMMUNICATION"]["ui_vision_sender_port"])
        self.server = udp_socket(host, port)

    def send_packet(self, p_packet):
        """ Envoi un seul paquet. """
        try:
            self.server.send(p_packet)
        except ConnectionRefusedError:
            # FIXME: hack
            pass

    def send_command(self, p_packets):
        """ Reçoit une liste de paquets et les envoies. """
        for packet in p_packets:
            self._send_packet(packet)
