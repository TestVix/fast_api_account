from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fast_api_account.domain_database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
