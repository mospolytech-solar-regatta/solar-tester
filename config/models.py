import json
from os import path

from pydantic import BaseModel

config_folder = 'configurations'
data_folder = 'test_data'
config_file_appendix = '_config.json'
data_file_appendix = '_test.json'
example_data_file_appendix = '_test_example.json'
test_script_appendix = '_script.py'
script_folder = 'scripts'


class SerialConfig(BaseModel):
    name: str = ''
    rate: int = 115200


class TestConfigBase(BaseModel):
    name: str = ''

    def get_config_path(self, dir_prefix=''):
        filename = f'{self.name}{config_file_appendix}'
        config_path = path.join(dir_prefix, config_folder, filename)
        return config_path

    def get_script_path(self, dir_prefix=''):
        filename = f'{self.name}{test_script_appendix}'
        config_path = path.join(dir_prefix, script_folder, filename)
        return config_path

    def get_data_path(self, dir_prefix=''):
        filename = f'{self.name}{data_file_appendix}'
        data_path = path.join(dir_prefix, data_folder, filename)
        if path.exists(data_path):
            return data_path
        filename = f'{self.name}{example_data_file_appendix}'
        data_path = path.join(dir_prefix, data_folder, filename)
        if path.exists(data_path):
            return data_path

        raise FileNotFoundError('data file not found')

    def save_config(self, dir_prefix=''):
        json_config = self.json()
        config_path = self.get_config_path(dir_prefix)
        with open(config_path, 'w') as cfg:
            cfg.write(json_config)

    def from_file(self, filename=None, dir_prefix=''):
        new_cfg = self
        if filename is None:
            filename = self.get_config_path(dir_prefix)
        if path.exists(filename):
            with open(filename) as f:
                cfg = json.loads(f.read())
                new_cfg = self.__class__(**cfg)
        new_cfg.save_config(dir_prefix)
        return new_cfg

    def get_data(self, filename=None, dir_prefix=''):
        if filename is None:
            filename = self.get_data_path(dir_prefix)
        with open(filename) as f:
            data = json.loads(f.read())
            return data


class BoatTestConfig(TestConfigBase):
    name: str = 'boat'
    serial_config: SerialConfig = SerialConfig()
