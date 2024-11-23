from typing import Optional
from src.database import models
from sqlmodel import select
from pydantic import BaseModel
from fastapi import HTTPException


class EmployeeResponse(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    hire_date: str
    job: str
    salary: float
    manager: Optional[str]
    department: str

    class Config:
       from_attributes = True


def select_emp_all(session, offset, limit):
    manager_alias = models.Employee.__table__.alias("me")
    statement = (
        select(
            models.Employee.employee_id,
            models.Employee.first_name,
            models.Employee.last_name,
            models.Employee.email,
            models.Employee.phone_number,
            models.Employee.hire_date,
            models.Employee.salary,
            models.Job.job_title.label("job"),
            models.Department.department_name.label("department"),
            manager_alias.c.first_name.label("manager"),
        )
        .join(models.Job, models.Employee.job_id == models.Job.job_id)
        .join(
            models.Department,
            models.Employee.department_id == models.Department.department_id,
        )
        .join(
            manager_alias,
            models.Employee.manager_id == manager_alias.c.employee_id,
            isouter=True,
        )
        .order_by(models.Employee.employee_id.asc())
        .offset(offset)
        .limit(limit)
    )
    results = session.exec(statement).all()

    response = [
        EmployeeResponse(
            employee_id=record.employee_id,
            first_name=record.first_name,
            last_name=record.last_name,
            email=record.email,
            phone_number=record.phone_number,
            hire_date=record.hire_date.isoformat(),
            job=record.job,
            salary=record.salary,
            manager=record.manager,
            department=record.department,
        )
        for record in results
    ]

    return response


def select_emp_byId(emp_id, session):
    manager_alias = models.Employee.__table__.alias("me")
    statement = (
        select(
            models.Employee.employee_id,
            models.Employee.first_name,
            models.Employee.last_name,
            models.Employee.email,
            models.Employee.phone_number,
            models.Employee.hire_date,
            models.Employee.salary,
            models.Job.job_title.label("job"),
            models.Department.department_name.label("department"),
            manager_alias.c.first_name.label("manager"),
        )
        .join(models.Job, models.Employee.job_id == models.Job.job_id)
        .join(
            models.Department,
            models.Employee.department_id == models.Department.department_id,
        )
        .join(
            manager_alias,
            models.Employee.manager_id == manager_alias.c.employee_id,
            isouter=True,
        )
        .where(models.Employee.employee_id == emp_id)
    )
    result = session.exec(statement).first()

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    response = EmployeeResponse(
        employee_id=result.employee_id,
        first_name=result.first_name,
        last_name=result.last_name,
        email=result.email,
        phone_number=result.phone_number,
        hire_date=result.hire_date.isoformat(),
        job=result.job,
        salary=result.salary,
        manager=result.manager,
        department=result.department,
    )

    return response
