from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "root"
PASS = "1234"
SERVER = "localhost"
PORT = "3306"
DB = "mysql"

# Connection pool برای بار همزمان (کمک به کاهش response time در Locust)
engine = create_engine(
    f"mysql+pymysql://{USER}:{PASS}@{SERVER}:{PORT}/{DB}",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class BookDB(Base):
    __tablename__ = "books"
    __table_args__ = (
        Index("ix_books_name", "name"),
        Index("ix_books_author", "author"),
    )
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    author = Column(String(100))
    year = Column(Integer)