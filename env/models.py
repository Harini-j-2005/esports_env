from pydantic import BaseModel
from typing import Dict, Any

class Observation(BaseModel):
    task: str
    state: Dict[str, Any]
    step_count: int

class Action(BaseModel):
    command: str

class Reward(BaseModel):
    value: float