import json
import os
import subprocess
from dataclasses import dataclass

from starlette.background import BackgroundTasks

from models import Status


class TestController:
    @dataclass
    class STATES:
        RUN = 1
        STOP = 2
        RESTART = 3

    State = STATES.RUN

    def terminate(self):
        self.State = TestController.STATES.STOP


class Runner:

    def __init__(self):
        self.pythopath = os.getcwd()
        self.processes = {}

    def run(self, cfg, background: BackgroundTasks):
        script = cfg.get_script()
        controller = TestController()
        background.add_task(script, controller=controller)
        self.processes[cfg.name] = controller

    def stop(self, cfg):
        if self.processes.get(cfg.name) is not None:
            self.processes[cfg.name].terminate()

    def stop_all(self):
        for proc in self.processes.values():
            proc.terminate()

    def get_running_procs(self) -> list:
        return list(self.processes.keys())
