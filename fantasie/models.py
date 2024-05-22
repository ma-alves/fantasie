from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
	pass


class CostumeAvailability(str, Enum):
	AVAILABLE = 'available'
	UNAVAILABLE = 'unavailable'


class Costume(Base):
	__tablename__ = 'costumes'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str]
	description: Mapped[str]
	fee: Mapped[float]
	availability: Mapped[CostumeAvailability]

	rental: Mapped[List['Rental']] = relationship(back_populates='costumes')


class Customer(Base):
	__tablename__ = 'customers'

	id: Mapped[int] = mapped_column(primary_key=True)
	cpf: Mapped[str] = mapped_column(String(11))
	name: Mapped[str]
	email: Mapped[str]
	phone_number: Mapped[str] = mapped_column(String(11))
	address: Mapped[str]

	rental: Mapped[List['Rental']] = relationship(back_populates='customers')


class Employee(Base):
	__tablename__ = 'employees'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str]
	email: Mapped[str]
	password: Mapped[str]
	phone_number: Mapped[Optional[str]] = mapped_column(String(11))

	rental: Mapped[List['Rental']] = relationship(back_populates='employees')


class Rental(Base):
	"""Neste formato o cliente não tem relação direta com o funcionário,
	apenas com o aluguel, que pelo seu registro liga o cliente ao
	funcionário indiretamente. Essa relação também ocorre da mesma
	forma com a fantasia, tendo a tabela 'Rental' como centro.
	"""

	__tablename__ = 'rental'

	id: Mapped[int] = mapped_column(primary_key=True)
	employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
	customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
	costume_id: Mapped[int] = mapped_column(ForeignKey('costumes.id'))
	rental_date: Mapped[datetime] = mapped_column(default=datetime.now())
	return_date: Mapped[datetime] = mapped_column(
		default=datetime.now() + timedelta(days=7)
	)

	employees: Mapped['Employee'] = relationship(back_populates='rental')
	customers: Mapped['Customer'] = relationship(back_populates='rental')
	costumes: Mapped['Costume'] = relationship(back_populates='rental')
