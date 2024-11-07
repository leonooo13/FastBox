import jwt
from pydantic import BaseModel
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import engine
from typing import Annotated
from fastapi import Depends, Form, Cookie, HTTPException
from fastapi.responses import RedirectResponse
from app.models.user import User
from app.schemas.user import UserRegister, Token


class TokenPayload(BaseModel):
    sub: int


def get_user_register(
        username: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
) -> UserRegister:
    return UserRegister(username=username, password=password, confirm_password=confirm_password)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_token_from_cookie(token: str = Cookie(None, alias="token")) -> str:
    if not token:
        return ""
    return token.split(" ")[1] if token.startswith("Bearer ") else token


#
#
def get_current_user(session: SessionDep, token: str = Depends(get_token_from_cookie)) -> User | None:
    try:
        # 解码 token 并验证
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
        user = session.get(User, token_data.sub)
        print(user)
        if not user:
            return None
        return user
    except Exception as e:
        return None


CurrentUser = Annotated[User|None, Depends(get_current_user)]
# CurrentUser = Depends(get_current_user)
