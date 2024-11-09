from pydantic import BaseModel
from datetime import date
from app.models.project import ProjectStatus
class ProjectCreate(BaseModel):
    name: str
    description: str
    deadline: date  # 或者其他类型
    status: ProjectStatus

