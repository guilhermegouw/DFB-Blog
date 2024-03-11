import pytest
from .factories import PostFactory, UserFactory



@pytest.fixture
def test_user():
    return UserFactory()

@pytest.fixture
def post_factory():
    return PostFactory(
        title="Test title",
        body="Test body",
        author=UserFactory(),
    )
