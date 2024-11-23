from fastapi import HTTPException
from sqlmodel import select
from src.database import models
from src.lib import crypt
import datetime

def sign_Up(session , user):
    session.add(models.Auth(
        username=user.username,
        password=crypt.hash_password(user.password),
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