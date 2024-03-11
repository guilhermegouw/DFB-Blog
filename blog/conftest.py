import pytest
from .factories import PostFactory


@pytest.fixture
def post_factory():
    return PostFactory
