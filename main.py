import datetime
import os
from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import SessionLocal
from models import AuthUser
from schemas import UserRegister, UserLogin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
import hashlib
from routers.auth import create_access_token
import base64
# import hashlib
import binascii
from fast_api_account.domain_database import domains, to_domains, http, index_number
# import 

def verify_django_password(raw_password: str, hashed_password: str) -> bool:
    algorithm, iterations, salt, hash_val = hashed_password.split('$')

    dk = hashlib.pbkdf2_hmac(
        'sha256',
        raw_password.encode(),
        salt.encode(),
        int(iterations)
    )
    calc_hash = binascii.hexlify(dk).decode()

    return calc_hash == hash_val

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=to_domains,   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    print('login keldi', flush=True)
    print(user, flush=True)
    db_user = db.query(AuthUser).filter(AuthUser.username == user.username).first()

    if not db_user or not verify_django_password(user.password, db_user.password):
        return  {"message": "Username yoki parol noto'g'ri"}
    access_token = create_access_token(data={"sub": db_user.username})
    # response = Response()
    response = JSONResponse(content={"message": "Login successful", 'redirect': "/"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60 * 24,
        samesite="lax",
        # domain=domains[index_number],
    )
    # print(access_token, flush=True)
    return response
    # return {"message": "Login successful", "username": db_user.username, "access_token": access_token}

@app.post("/register/")
def register(user: UserRegister, db: Session = Depends(get_db)):
    print('registerdwdwdwd', flush=True)
    print(app.add_middleware, flush=True)
    # print('salom', flush=True)
    # print(user, flush=True)
    if user.username == '' or user.password1 == '' or user.password2 == '' or user.fio == '' or user.email == '':
        return {"message": "Barcha maydonlar to'ldirilishi shart"}

    if len(user.password1) < 8:
        return {"message": "Parol kamida 8 ta belgidan iborat bo'lishi kerak"}
    if user.password1 != user.password2:
        return {"message": "Parollar mos emas"}
    password = user.password1

# Bo'sh joy borligini tekshirish
    if any(c.isspace() for c in password):
        return {"message": "Parolda bo'sh joy bo'lmasligi kerak"}

    # Katta harf, kichik harf, raqam borligini tekshirish
    # if not any(c.isupper() for c in password):
    #     return {"message": "Parolda kamida bitta KATTA harf bo'lishi kerak"}

    # if not any(c.islower() for c in password):
    #     return {"message": "Parolda kamida bitta kichik harf bo'lishi kerak"}

    # if not any(c.isdigit() for c in password):
    #     return {"message": "Parolda kamida bitta raqam bo'lishi kerak"}
    db_user = db.query(AuthUser).filter(AuthUser.username == user.username).first()
    if db_user:
        return {"message": "Username allaqachon mavjud"}

    # Django-style salt (NOT base64)
    salt = binascii.hexlify(os.urandom(6)).decode()   # 12-character salt

    iterations = 260000

    dk = hashlib.pbkdf2_hmac(
        'sha256',
        user.password1.encode(),
        salt.encode(),
        iterations
    )

    hashed_password = f"pbkdf2_sha256${iterations}${salt}${binascii.hexlify(dk).decode()}"

    new_user = AuthUser(
        username=user.username, 
        password=hashed_password,
        first_name=user.fio,
        last_name='',
        email=user.email,
        # phone=user.telefon,
        is_active=True,
        is_staff=False,
        is_superuser=False,
        date_joined = datetime.datetime.now(),
        phone = 'telefon'
        # istaff=False,
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.username})
    response = JSONResponse(content={"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz", 'redirect': "/"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60 * 24,
        samesite="lax",
        # domain=domains[index_number],
    )
    return response

# @app.get('/login/')
# def login(user: UserLogin = None, req: dict = None):
#     if req

#     return {"message": "Iltimos, login qiling"}