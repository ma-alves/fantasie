from .schemas import Message

from fastapi import FastAPI

app = FastAPI()

@app.get('/', status_code=200, response_model=Message)
def index():
    return {'message': 'Welcome to Fantasie!'}
