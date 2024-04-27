from typing import Annotated

from fantasie.database import get_session
from fantasie.models import Employee
from fantasie.schemas import EmployeeInput, EmployeeList, EmployeeOutput, Message
from fantasie.security import get_password_hash

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]

@app.get('/', response_model=Message, status_code=200)
def index():
    return {'message': 'Welcome to Fantasie!'}


@app.get('/employees/', response_model=EmployeeList)
def read_employees(session: SessionDep, skip: int = 0, limit: int = 100):
    employees = session.scalars(
        select(Employee).offset(skip).limit(limit)
    ).all()

    return {'employees': employees}


@app.post('/employees/', response_model=EmployeeOutput, status_code=201)
def create_employee(employee: EmployeeInput, session: SessionDep):
    db_employee = session.scalar(
        select(Employee).where(Employee.email == employee.email)
    )
    if db_employee:
        raise HTTPException(400, detail='Employee already registered.')
    
    hashed_password = get_password_hash(employee.password)
    
    db_employee = Employee(
        name=employee.name,
        email=employee.email,
        password=hashed_password,
        phone_number=employee.phone_number
    )

    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)

    return db_employee
