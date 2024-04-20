from pydantic import BaseModel, EmailStr
from typing import List


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
