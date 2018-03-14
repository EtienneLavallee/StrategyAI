# Under MIT License, see LICENSE.txt

import logging
import time
from multiprocessing import Queue, Manager
import signal

from Engine.engine import Engine
from ai.coach import Coach


class Framework:

    QUEUE_SIZE = 100

    def __init__(self, cli_args):

        self.logger = logging.getLogger(self.__class__.__name__)

        self.game_state = Manager().dict()
        self.field = Manager().dict()

        self.ai_queue = Queue(maxsize=Framework.QUEUE_SIZE)
        self.referee_queue = Queue(maxsize=Framework.QUEUE_SIZE)
        self.ui_send_queue = Queue(maxsize=Framework.QUEUE_SIZE)
        self.ui_recv_queue = Queue(maxsize=Framework.QUEUE_SIZE)

        self.engine = Engine(self.game_state,
                             self.field,
                             self.ai_queue,
                             self.referee_queue,
                             self.ui_send_queue,
                             self.ui_recv_queue)

        self.coach = Coach(self.game_state,
                           self.field,
                           self.ai_queue,
                           self.referee_queue,
                           self.ui_send_queue,
                           self.ui_recv_queue)

        self.engine.fps = cli_args.engine_fps

        if cli_args.on_negative_side:
            self.engine.on_negative_side = True

        if cli_args.unlock_engine_fps:
            self.engine.unlock_fps()

        if cli_args.enable_profiling:
            self.coach.enable_profiling()
            self.engine.enable_profiling()

    def start(self):

        self.engine.start()
        self.coach.start()

        # end signal - do you like to stop gracefully? DO NOT MOVE! MUST BE PLACED AFTER PROCESSES
        signal.signal(signal.SIGINT, lambda *args: self.stop_game())

        # stop until someone manually stop us / we receive interrupt signal from os
        # also check if one of the subprocess died
        every_process_is_alright = True
        while every_process_is_alright:
            every_process_is_alright = self.engine.is_alive() and \
                                       self.coach.is_alive() and \
                                       not self.engine.is_any_subprocess_borked()
            if not every_process_is_alright:
                self.logger.critical('One of the engine subprocesses died! Shutting down...')
                self.engine.terminate_subprocesses()
                self.engine.terminate()
                self.coach.terminate()

            # use the time you want here, 0.5 seems sane to me.
            time.sleep(0.5)

        self.stop_game()

    def stop_game(self):
        self.engine.terminate()
        self.coach.terminate()
        raise SystemExit('Stop Game')
