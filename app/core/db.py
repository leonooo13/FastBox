from sqlmodel import create_engine

DATABASE_URL = "sqlite:///./FastBox.db"
engine = create_engine(DATABASE_URL, echo=True)
