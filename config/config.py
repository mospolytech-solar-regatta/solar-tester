import json

from constants import available_configs


class Config:
    _cfg_classes = {}
    _available_configs = {}

    def __init__(self, *config_cls):
        self.load_configs(*config_cls)

    def load_configs(self, *config_cls):
        if len(config_cls) == 0:
            config_cls = available_configs
        for cfg in config_cls:
            conf = cfg().from_file()
            self._cfg_classes[conf.name] = conf.__class__
            self._available_configs[conf.name] = conf

    def get_test_config_model(self, name: str):
        m = self._available_configs.get(name, None)
        if m is None:
            raise NotImplementedError('test config not found')

    def unmarshal_config(self, name: str, cfg: str):
        cls = self.get_test_config_model(name)
        return self._unmarshal_config(cfg, cls)

    @staticmethod
    def _unmarshal_config(cfg, cfg_cls):
        cfg = json.loads(cfg)
        return cfg_cls(**cfg)

    def update_config(self, name, cfg):
        if type(self._cfg_classes[name]) != type(cfg):
            raise AssertionError('config class not valid for this config name')

    def get_config(self, name):
        return self._available_configs.get(name, None)

    def get_data(self, name, filename=None):
        cfg = self.get_config(name)
        return cfg.get_data(filename)
