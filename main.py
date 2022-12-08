import logging
from typing import List
from fastapi import FastAPI, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Body, BackgroundTasks, Depends
from fastapi.responses import HTMLResponse
import testing
from config.config import Config
from fastapi import WebSocket

from dependencies import get_listener
from listener.listener import Listener
from responses import listener_response

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def post_config(test_name: str, cfg=Body(default='')):
    cfg = config.unmarshal_config(test_name, cfg)
    config.update_config(test_name, cfg)
    return 'OK'


@app.get('/config/{test_name}')
async def get_config(test_name: str):
    return config.get_config(test_name)


@app.get('/run/{test_name}')
async def get_run(test_name: str, background_tasks: BackgroundTasks):
    cfg = config.get_config(test_name)
    runner.run(cfg, background_tasks)
    return 'ok'


@app.get('/stop/{test_name}')
async def get_run(test_name: str):
    cfg = config.get_config(test_name)
    runner.stop(cfg)
    return 'ok'


@app.websocket('/listen/{channel}')
async def websocket_endpoint(channel: str, websocket: WebSocket, listener: Listener = Depends(get_listener)):
    await websocket.accept()
    await listener.listen(channel, websocket)


@app.get("/listen")
async def get():
    return HTMLResponse(listener_response)
