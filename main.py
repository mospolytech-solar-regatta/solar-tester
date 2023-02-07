import logging
import os.path
from typing import List

from fastapi import FastAPI, Body, BackgroundTasks, Depends
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

import testing
from config.config import Config
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

# app.mount("/app", StaticFiles(directory="front/dist", html=True, check_dir=False), name="app")
app.mount("/assets", StaticFiles(directory="front/dist/assets", check_dir=False), name="assets")
app.mount("/vendor", StaticFiles(directory="front/dist/vendor", check_dir=False), name="vendor")

config = Config()
logging.info("testing initialized")
runner = testing.Runner()
logging.info("runner initialized")


@app.on_event("shutdown")
def shutdown_event():
    runner.stop_all()


@app.get("/")
async def root():
    return RedirectResponse("/app")


@app.api_route('/app/{path_name:path}')
async def front(path_name):
    front_path = 'front/dist/index.html'
    error_path = 'static/frontend_not_compiled.html'
    if os.path.exists(front_path):
        response = FileResponse(front_path)
    else:
        response = FileResponse(error_path)
    return response


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
