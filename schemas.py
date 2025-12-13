from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password1: str
    password2: str
    fio: str 
    email: str
    # telefon: str
class UserLogin(BaseModel):
    username: str
    password: str