import datetime
from typing import Union
import jwt
import os

ACCESS_TOKEN_EXPIRE_MINUTES_DEFAULT = 1440 # 1d

def create_access_token(data: dict, expires_delta: Union[datetime.timedelta, None] = None):
    """
    สร้าง JWT Token ด้วยข้อมูล payload และเวลาหมดอายุ

    Parameters:
        data (dict): ข้อมูล payload ที่ต้องการใส่ใน JWT
        expires_delta (Union[datetime.timedelta, None]): เวลาที่ token จะหมดอายุ

    Returns:
        str: JWT token ที่สร้าง
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES_DEFAULT)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('JWT_SECRET_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))
    
    return encoded_jwt