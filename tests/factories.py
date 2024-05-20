from random import randint

import factory
import factory.fuzzy

from fantasie.models import Costume, CostumeAvailability, Customer, Employee


class EmployeeFactory(factory.Factory):
    class Meta:
        model = Employee

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('name', locale='pt_BR')
    email = factory.Faker('free_email')
    password = factory.LazyAttribute(lambda obj: f'{obj.name}1234')
    phone_number = factory.Faker('phone_number')


class CostumeFactory(factory.Factory):
    class Meta:
        model = Costume

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('name', locale='pt_BR')
    description = factory.Faker('text')
    fee = float(randint(0,1000))
    availability = factory.fuzzy.FuzzyChoice(CostumeAvailability)


class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer

    id = factory.Sequence(lambda n: n + 1)
    cpf = factory.Faker('random_number', digits=11, fix_len=True)
    name = factory.Faker('name', locale='pt_BR')
    email = factory.Faker('free_email')
    phone_number = factory.Faker('phone_number')
    address = factory.Faker('address', locale='pt_BR')
