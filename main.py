from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth, emp
from src.database import db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup")
    db.create_db_and_tables()
    yield
    print("shutdown")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.auth_router, prefix="/api/v0")
app.include_router(emp.emp_router, prefix="/api/v0")
