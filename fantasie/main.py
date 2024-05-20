from fantasie.schemas import Message
from fantasie.routes import employees, auth, costumes

from fastapi import FastAPI


app = FastAPI()

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(costumes.router)


@app.get('/', response_model=Message, status_code=200)
def index():
    return {'message': 'Welcome to Fantasie!'}
