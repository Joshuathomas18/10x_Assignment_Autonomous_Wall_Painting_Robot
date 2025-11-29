from pydantic import BaseModel, Field
from typing import List, Optional

class ObstacleData(BaseModel):
    x: float
    y: float
    width: float
    height: float

class WallRequest(BaseModel):
    wall_width: float = Field(..., gt=0, description="Width in meters")
    wall_height: float = Field(..., gt=0, description="Height in meters")
    tool_size: float = Field(0.1, gt=0, description="Robot tool size in meters")
    obstacles: List[ObstacleData] = []

class JobResponse(BaseModel):
    job_id: int
    status: str
    message: str

class TrajectoryResponse(BaseModel):
    job_id: int
    status: str
    path: Optional[List[dict]] = None

