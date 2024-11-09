from typing import List

from sqlmodel import Session, select
from app.models.project import Project
from app.schemas.project import ProjectCreate
from app.routes.deps import SessionDep

class ProjectCrude:
    def __init__(self, db_session: Session):
        self.session = db_session
    def create(self, project: ProjectCreate) -> Project:
        project = Project(**project.model_dump())
        print(project)
        print(project.__dict__)
        self.session.add(project)
        self.session.commit()
        return project
    def get_all_projects(self) -> List[Project]:
        # 获取所有项目
        statement = select(Project).order_by(Project.created_at)
        projects = self.session.exec(statement).all()
        return list(projects)