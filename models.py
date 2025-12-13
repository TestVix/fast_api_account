from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class AuthUser(Base):
    __tablename__ = "myapp_authuser"   # Django jadvali

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(128))
    last_login = Column(DateTime)
    is_superuser = Column(Boolean)
    username = Column(String(150))
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String(254))
    is_staff = Column(Boolean)
    is_active = Column(Boolean)
    phone = Column(String(15))
    date_joined = Column(DateTime)
