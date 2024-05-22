from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fantasie.database import get_session
from fantasie.models import Employee
from fantasie.schemas import (
	EmployeeInput,
	EmployeeList,
	EmployeeOutput,
	Message,
)
from fantasie.security import get_password_hash, get_current_employee


router = APIRouter(prefix='/employees', tags=['employees'])

CurrentEmployee = Annotated[Employee, Depends(get_current_employee)]
SessionDep = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=EmployeeList)
def read_employees(session: SessionDep, skip: int = 0, limit: int = 100):
	employees = session.scalars(
		select(Employee).offset(skip).limit(limit)
	).all()

	return {'employees': employees}


@router.get('/{employee_id}', response_model=EmployeeOutput, status_code=200)
def read_employee(session: SessionDep, employee_id: int):
	employee = session.scalar(
		select(Employee).where(Employee.id == employee_id)
	)

	if not employee:
		raise HTTPException(404, detail='Employee not registered.')

	return employee


@router.post('/', response_model=EmployeeOutput, status_code=201)
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
		phone_number=employee.phone_number,
	)

	session.add(db_employee)
	session.commit()
	session.refresh(db_employee)

	return db_employee


@router.put('/{employee_id}', response_model=EmployeeOutput)
def update_employee(
	current_employee: CurrentEmployee,
	session: SessionDep,
	employee: EmployeeInput,
	employee_id: int,
):
	if current_employee.id != employee_id:
		raise HTTPException(status_code=400, detail='Not enough permissions')

	current_employee.name = employee.name
	current_employee.password = get_password_hash(employee.password)
	current_employee.email = employee.email
	current_employee.phone_number = employee.phone_number
	session.commit()
	session.refresh(current_employee)

	return current_employee


@router.delete('/{employee_id}', response_model=Message)
def delete_employee(
	current_employee: CurrentEmployee,
	session: SessionDep,
	employee_id: int,
):
	if current_employee.id != employee_id:
		raise HTTPException(status_code=400, detail='Not enough permissions')

	session.delete(current_employee)
	session.commit()

	return {'message': 'Employee deleted.'}
