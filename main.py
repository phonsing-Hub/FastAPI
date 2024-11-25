from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth, emp
from src.database import db
from contextlib import asynccontextmanager

# จำลองฟังก์ชันสำหรับดึง role ของผู้ใช้งาน
def get_current_user_role():
    # ตรงนี้ควรดึงจาก JWT token หรือฐานข้อมูล
    return "admin"  # เปลี่ยนเป็น role จริงในโปรเจกต์จริง

# ฟังก์ชันสำหรับตรวจสอบสิทธิ์
def check_permissions(role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

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
app.include_router(
    emp.emp_router,
    prefix="/api/v0/employees",
    dependencies=[Depends(check_permissions)],
) 
