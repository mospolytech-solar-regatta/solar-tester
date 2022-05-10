import json
import os
import subprocess

from models import Status


class Runner:

    def __init__(self):
        self.pythopath = os.getcwd()
        self.processes = {}
        with open('status.tmp', 'w') as f:
            st = Status()
            f.write(st.json())

    def run(self, cfg):
        script_path = cfg.get_script_path()
        proc = subprocess.Popen(
            f'PYTHONPATH={self.pythopath} {script_path}',
            shell=True)
        self.processes[cfg.name] = proc

    def stop(self, cfg):
        self.processes[cfg.name].terminate()

    def stop_all(self):
        for proc in self.processes.values():
            proc.terminate()

    def get_status(self) -> Status:
        with open('status.tmp') as f:
            st = json.loads(f.read())
            st = Status(**st)
            return st

    def get_running_procs(self) -> list:
        return self.processes.keys()
