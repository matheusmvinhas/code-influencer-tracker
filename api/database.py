from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração direta
DATABASE_URL = "postgresql://admin:admin@postgres:5432/influencer_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependência para injeção no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()