from typing import Annotated, List
from fastapi import APIRouter, Query
from src.database import db
from src.controllers import ctl_emp

emp_router = APIRouter()

@emp_router.get("/", response_model=List[ctl_emp.EmployeeResponse])
def emp_router_get(    
    session: db.SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=500)] = 100,):
    employess = ctl_emp.select_emp_all(session, offset, limit)
    return employess

@emp_router.get("/{emp_id}", response_model=ctl_emp.EmployeeResponse)
def emp_router_get_byId(emp_id: int, session: db.SessionDep):
    employessId = ctl_emp.select_emp_byId(emp_id, session)
    return employessId