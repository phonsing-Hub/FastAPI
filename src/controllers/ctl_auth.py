from fastapi import HTTPException
from sqlmodel import select
from src.database import models
from src.lib import crypt
import re
import datetime

def sign_Up(session , user):
    if not user.username.strip() or not user.password.strip():
        raise HTTPException(status_code=400, detail="username or password is null")
    # ตรวจสอบความยาว username
    if len(user.username) < 4:
        raise HTTPException(status_code=400, detail="username must be at least 4 characters")
    # ตรวจสอบความยาว password
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="password must be at least 6 characters")
    # ตรวจสอบ password ด้วย regex
    password_pattern = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{6,}$"
    if not re.match(password_pattern, user.password):
        raise HTTPException(
            status_code=400, 
            detail="password must contain at least one letter, one digit, and one special character"
        )
    session.add(models.Auth(
        username=user.username,
        password=crypt.hash_password(user.password),
        role=user.role,
        last_login=datetime.datetime.now()
    ))
    session.commit()


def sign_In(session, user):
    auth = select(models.Auth).where(models.Auth.username == user.username)
    results = session.exec(auth).first()
    if not results:
        raise HTTPException(status_code=404, detail="User not found")

    if not crypt.verify_password(user.password, results.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    return results