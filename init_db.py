from app.core.db import engine
from sqlmodel import SQLModel
from app.models.user import User
if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)