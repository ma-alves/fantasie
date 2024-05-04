from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fantasie.database import get_session
from fantasie.models import Employee
from fantasie.schemas import Token
from fantasie.security import (
    create_access_token,
    get_current_employee,
    verify_password_hash,
)

OAuth2Password = Annotated[OAuth2PasswordRequestForm, Depends()]
SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/', response_model=Token)
def login_for_access_token(form_data: OAuth2Password, session: SessionDep):
    employee = session.scalar(
        select(Employee).where(Employee.email == form_data.email)
    )

    if not employee:
        raise HTTPException(404, detail='Employee not registered.')
    
    if not verify_password_hash(form_data.password, employee.password):
        raise HTTPException(400, detail='Incorrect email or password.')
    
    access_token = create_access_token(data={'sub': employee.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    employee: Employee = Depends(get_current_employee)
):
    new_access_token = create_access_token(data={'sub': employee.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
