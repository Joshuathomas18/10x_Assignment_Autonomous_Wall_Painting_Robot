from sqlalchemy import Column, Integer, Float, String, DateTime, LargeBinary, Index
from sqlalchemy.sql import func
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    wall_width = Column(Float, nullable=False)
    wall_height = Column(Float, nullable=False)
    
    # Status: PENDING, COMPLETED, FAILED
    status = Column(String, default="PENDING", index=True)
    
    # Store compressed path data as BLOB instead of text - saves space
    path_data = Column(LargeBinary, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index('idx_jobs_status_created', 'status', 'created_at'),
    )

    def __repr__(self):
        return f"<Job(id={self.id}, status={self.status})>"

