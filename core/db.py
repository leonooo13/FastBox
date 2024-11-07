from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///./test.db"  # SQLite 数据库路径
engine = create_engine(DATABASE_URL, echo=True)