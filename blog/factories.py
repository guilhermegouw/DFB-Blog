import factory
from django.contrib.auth import get_user_model

from .models import Post


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=3)
    body = factory.Faker("paragraph", nb_sentences=3)
    author = factory.SubFactory(UserFactory)
