import factory

from fantasie.models import Employee


class EmployeeFactory(factory.Factory):
    class Meta:
        model = Employee

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.LazyAttribute(lambda obj: f'{obj.name}1234')
    phone_number = factory.Faker('phone_number')
    