from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.controllers import ctl_auth
from src.database import db
from src.lib import jwt
import datetime
import os

auth_router = APIRouter()


class Auth(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    username: str
    role: str

    class Config:
        from_attributes = True


@auth_router.post("/signin", response_model=AuthResponse)
def auth_signin(session: db.SessionDep, user: Auth, res: Response):
    try:
        result = ctl_auth.sign_In(session, user)
        access_token_expires = datetime.timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')))
        token = jwt.create_access_token(
            data={
                "name": result.username,
                "role": result.role
                }, 
            expires_delta=access_token_expires
        )
        res.set_cookie(
            key="APL_TOKEN", 
            value=token, 
            max_age=access_token_expires,
            expires=datetime.datetime.now(datetime.timezone.utc) + access_token_expires,
            httponly=True, 
            secure=True,
            samesite="Strict"
        )
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@auth_router.post("/signup")
def auth_signup(session: db.SessionDep, user: Auth):
    try:
        ctl_auth.sign_Up(session, user)
        return JSONResponse(status_code=201, content={"message": "success"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
