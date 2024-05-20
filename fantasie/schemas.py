from pydantic import BaseModel, EmailStr
from typing import List

from fantasie.models import CostumeAvailability


class Message(BaseModel):
    message: str


# Tokens
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


# Employees
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


# Costumes
class CostumeInput(BaseModel):
    name: str
    description: str
    fee: float
    availability: CostumeAvailability


class CostumeOutput(BaseModel):
    name: str
    description: str
    fee: float
    availability: CostumeAvailability


class CostumeList(BaseModel):
    costumes: List[CostumeOutput]
