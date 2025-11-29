import json
import zlib
import structlog
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import Job
from app.core.planner import CoveragePlanner
from app.api.schemas import WallRequest, JobResponse, TrajectoryResponse

router = APIRouter()
logger = structlog.get_logger()

async def compute_path(job_id: int, request: WallRequest):
    from app.db.database import AsyncSessionLocal
    
    log = logger.bind(job_id=job_id)
    log.info("task_started", wall_size=f"{request.wall_width}x{request.wall_height}")

    try:
        planner = CoveragePlanner(request.wall_width, request.wall_height, request.tool_size)
        for obs in request.obstacles:
            planner.add_obstacle(obs.x, obs.y, obs.width, obs.height)
        
        path_list = planner.plan_path()
        
        path_json = json.dumps(path_list).encode('utf-8')
        compressed = zlib.compress(path_json)

        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Job).where(Job.id == job_id))
            job = result.scalar_one()
            job.status = "COMPLETED"
            job.path_data = compressed
            await db.commit()
            
        log.info("task_completed", points_generated=len(path_list))

    except Exception as e:
        log.error("task_failed", error=str(e))

@router.post("/plan", response_model=JobResponse)
async def submit_job(
    request: WallRequest, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    new_job = Job(
        wall_width=request.wall_width,
        wall_height=request.wall_height,
        status="PENDING"
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)

    background_tasks.add_task(compute_path, new_job.id, request)

    return {
        "job_id": new_job.id,
        "status": "PENDING",
        "message": "Calculation started in background."
    }

@router.get("/trajectory/{job_id}", response_model=TrajectoryResponse)
async def get_trajectory(job_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        response = {"job_id": job.id, "status": job.status}

        if job.status == "COMPLETED" and job.path_data:
            decompressed = zlib.decompress(job.path_data)
            response["path"] = json.loads(decompressed)
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error("trajectory_error", job_id=job_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error fetching trajectory")

