from sqlalchemy import Column, String
from .database import Base
from pydantic import BaseModel

class Run(Base):
    __tablename__ = "runs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String)
    current_stage = Column(String)

class StartRunRequest(BaseModel):
    brief: str