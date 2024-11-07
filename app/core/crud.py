import traceback

from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import get_password_hash, verify_password


def create_user(user_data: UserRegister, session: Session) -> User:
    # 创建 User 实例

    statement = select(User).where((User.name == user_data.username))
    existing_user = session.exec(statement).first()
    if existing_user:
        raise ValueError("User already exists")
    user = User(
        name=user_data.username,  # 假设你的 User 模型中有 name 字段
        password=get_password_hash(user_data.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def authenticate(session: Session, username: str, password: str) -> User | None:
    statement = select(User).where((User.name == username))
    db_user = session.exec(statement).first()
    if not db_user:
        return None
    if verify_password(password, db_user.password):
        return db_user
    else:
        return None

def get_all_users(session: Session) -> list[User]:
    statement = select(User)
    users = session.exec(statement).all()  # 获取所有用户
    return list(users)
