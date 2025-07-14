from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from fantasie.database import get_session
from fantasie.models import Employee
from fantasie.schemas import TokenData
from fantasie.settings import Settings

settings = Settings()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_password_hash(password: str):
	return pwd_context.hash(password)


def verify_password_hash(plain_password: str, hashed_password: str):
	return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
	to_encode = data.copy()
	expire = datetime.utcnow() + timedelta(
		days=settings.ACCESS_TOKEN_EXPIRE_DAYS
	)
	to_encode.update({'exp': expire})
	encoded_jwt = encode(
		payload=to_encode,
		key=settings.SECRET_KEY,
		algorithm=settings.ALGORITHM,
	)

	return encoded_jwt


async def get_current_employee(
	session: Session = Depends(get_session),
	token: str = Depends(oauth2_scheme),
):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Could not validate credentials',
		headers={'WWW-Authenticate': 'Bearer'},
	)

	try:
		payload = decode(
			jwt=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
		)
		email = payload.get('sub')
		if not email:
			raise credentials_exception
		token_data = TokenData(email=email)
	except DecodeError:
		raise credentials_exception
	except ExpiredSignatureError:
		raise credentials_exception

	employee = session.scalar(
		select(Employee).where(Employee.email == token_data.email)
	)

	if employee is None:
		raise credentials_exception

	return employee
