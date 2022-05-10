import logging
from typing import List

from fastapi import FastAPI

import testing
from config.config import Config

app = FastAPI()
config = Config()
logging.info("testing initialized")
runner = testing.Runner()
logging.info("runner initialized")


@app.on_event("shutdown")
def shutdown_event():
    runner.stop_all()


@app.get("/")
async def root():
    return {"message": "Hello It's testing here"}


@app.get("/status", response_model=List[str])
async def get_status():
    return runner.get_status()


@app.get('/config/reload')
async def test():
    config.load_configs()
    return 'ok'


@app.post('/config/{test_name}')
async def post_config(test_name: str, config):
    cfg = config.unmarshal_config(test_name, config)
    config.update_config(cfg)
    return 'OK'


@app.get('/config/{test_name}')
async def get_config(test_name: str):
    return config.get_config(test_name)


@app.get('/run/{test_name}')
async def get_run(test_name: str):
    cfg = config.get_config(test_name)
    runner.run(cfg)
    return 'ok'


@app.get('/stop/{test_name}')
async def get_run(test_name: str):
    cfg = config.get_config(test_name)
    runner.stop(cfg)
    return 'ok'
