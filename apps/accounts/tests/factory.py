from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from factory import Sequence, PostGenerationMethodCall
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from faker import Faker

fake = Faker()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f'{fake.unique.first_name().lower()}_{fake.random_int(min=100)}'
    email = fake.email()
    phone_number = Sequence(lambda n: f'100000000{n}')
    avatar = None
    date_verified = timezone.now()
    gender = FuzzyChoice(['m', 'f'])
    password = PostGenerationMethodCall('set_password', 'password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use set_password."""
        kwargs['password'] = make_password('password')
        return super()._create(model_class, *args, **kwargs)