from typing import Annotated

from fantasie.database import get_session
from fantasie.schemas import Message
from .routes import employees

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()
SessionDep = Annotated[Session, Depends(get_session)]

app.include_router(employees.router)

@app.get('/', response_model=Message, status_code=200)
def index():
    return {'message': 'Welcome to Fantasie!'}
