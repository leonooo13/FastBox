from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=50)
    email: str = Field(max_length=50, nullable=True)
    password: str = Field(max_length=50)



