from pydantic import BaseModel


class Status(BaseModel):
    boat_running: bool = False
    ground_running: bool = False
