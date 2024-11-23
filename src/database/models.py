from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, datetime

class Auth(SQLModel, table=True):
    __tablename__ = "authentication"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    password: str  # รหัสผ่านที่เก็บเป็น Hash
    role: str = Field(default="user", nullable=False) 
    last_login: Optional[datetime] = Field(default=None, nullable=True)
    last_logout: Optional[datetime] = Field(default=None, nullable=True)
   

class Region(SQLModel, table=True):
    __tablename__ = "regions"  # ชื่อตารางเป็น "regions"
    
    region_id: Optional[int] = Field(default=None, primary_key=True)
    region_name: Optional[str] = Field(max_length=25)

    # กำหนดความสัมพันธ์กับตาราง countries
    countries: List["Country"] = Relationship(back_populates="region")


class Country(SQLModel, table=True):
    __tablename__ = "countries"  # ชื่อตารางเป็น "countries"
    
    country_id: str = Field(primary_key=True, max_length=2)
    country_name: Optional[str] = Field(max_length=40)
    region_id: int = Field(foreign_key="regions.region_id")  # กำหนด Foreign Key ชี้ไปยัง regions.region_id

    # กำหนดความสัมพันธ์กับตาราง regions
    region: Optional[Region] = Relationship(back_populates="countries")
    
    # เพิ่มความสัมพันธ์กับ Location
    locations: List["Location"] = Relationship(back_populates="country")


class Location(SQLModel, table=True):
    __tablename__ = "locations"  # ชื่อตารางเป็น "locations"

    location_id: Optional[int] = Field(default=None, primary_key=True)
    street_address: Optional[str] = Field(max_length=40)
    postal_code: Optional[str] = Field(max_length=12)
    city: str = Field(max_length=30)
    state_province: Optional[str] = Field(max_length=25)
    country_id: str = Field(foreign_key="countries.country_id")  # แก้ไขชื่อ foreign key ให้ตรง

    country: Optional[Country] = Relationship(back_populates="locations")  # กำหนดความสัมพันธ์ย้อนกลับ
    departments: List["Department"] = Relationship(back_populates="location")


class Department(SQLModel, table=True):
    __tablename__ = "departments"  # ชื่อตารางเป็น "departments"

    department_id: Optional[int] = Field(default=None, primary_key=True)
    department_name: str = Field(max_length=30)
    location_id: Optional[int] = Field(foreign_key="locations.location_id")  # แก้ไขชื่อ foreign key ให้ตรง

    location: Optional[Location] = Relationship(back_populates="departments")
    employees: List["Employee"] = Relationship(back_populates="department")


class Job(SQLModel, table=True):
    __tablename__ = "jobs"  # ชื่อตารางเป็น "jobs"

    job_id: Optional[int] = Field(default=None, primary_key=True)
    job_title: str = Field(max_length=35)
    min_salary: Optional[float] = Field(default=None)
    max_salary: Optional[float] = Field(default=None)

    employees: List["Employee"] = Relationship(back_populates="job")


class Employee(SQLModel, table=True):
    __tablename__ = "employees"  # ชื่อตารางเป็น "employees"

    employee_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str] = Field(max_length=20)
    last_name: str = Field(max_length=25)
    email: str = Field(max_length=100)
    phone_number: Optional[str] = Field(max_length=20)
    hire_date: date
    job_id: int = Field(foreign_key="jobs.job_id")  # แก้ไขชื่อ foreign key ให้ตรง
    salary: float
    manager_id: Optional[int] = Field(foreign_key="employees.employee_id")  # แก้ไขชื่อ foreign key ให้ตรง
    department_id: Optional[int] = Field(foreign_key="departments.department_id")  # แก้ไขชื่อ foreign key ให้ตรง

    job: Optional[Job] = Relationship(back_populates="employees")
    department: Optional[Department] = Relationship(back_populates="employees")
    manager: Optional["Employee"] = Relationship(back_populates="subordinates", sa_relationship_kwargs={"remote_side": "Employee.employee_id"})
    subordinates: List["Employee"] = Relationship(back_populates="manager", sa_relationship_kwargs={"remote_side": "Employee.manager_id"})
    dependents: List["Dependent"] = Relationship(back_populates="employee")


class Dependent(SQLModel, table=True):
    __tablename__ = "dependents"  # ชื่อตารางเป็น "dependents"

    dependent_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    relationship: str = Field(max_length=25)
    employee_id: int = Field(foreign_key="employees.employee_id")  # แก้ไขชื่อ foreign key ให้ตรง

    employee: Optional[Employee] = Relationship(back_populates="dependents")
