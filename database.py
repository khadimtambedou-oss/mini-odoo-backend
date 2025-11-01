from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# 👉 Tu peux utiliser SQLite pendant le développement
DATABASE_URL = "sqlite:///./app.db"

# 👉 Si tu veux PostgreSQL plus tard, on remplacera par :
# DATABASE_URL = "postgresql://user:password@localhost/mini_odoo"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Dependency injection for FastAPI
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
