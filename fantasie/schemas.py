from pydantic import BaseModel, EmailStr
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class Message(BaseModel):
    message: str


class EmployeeInput(BaseModel):
    name: str
    password: str
    email: EmailStr
    phone_number: str


class EmployeeOutput(BaseModel):
    name: str
    email: EmailStr
    phone_number: str


class EmployeeList(BaseModel):
    employees: List[EmployeeOutput]
