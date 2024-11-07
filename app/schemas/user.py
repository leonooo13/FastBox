from typing import Optional

from pydantic import BaseModel, ConfigDict,validator
from fastapi import FastAPI, Request, Form, HTTPException

class UserRegister(BaseModel):
    username: str
    password: str
    confirm_password: str = Form(...)

    def validate_password_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')

class UserResponse(BaseModel):
    id: int
    name: str
    email: str | None
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserLogin(BaseModel):
    username: str
    password: str
    remember: bool
