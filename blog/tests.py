from django.urls import reverse
from .conftest import PostFactory

def test_home_status_code(client, db):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


def test_home_template(client, db):
    url = reverse("home")
    response = client.get(url)
    templates_found = [template.name for template in response.templates]
    assert "home.html" in templates_found


def test_home_template_content(client, db):
    post = PostFactory(title='Blog post title', body='Blog post body')
    url = reverse("home")
    response = client.get(url)
    assert "Django Blog" in str(response.content)
    assert post.title in str(response.content)
    assert post.body in str(response.content)



def test_detail_status_code(client, db):
    post = PostFactory()
    url = reverse("detail", kwargs={"pk": post.pk})
    response = client.get(url)
    assert response.status_code == 200

def test_detail_unexisting_post(client, db):
    post = PostFactory()
    url = reverse("detail", kwargs={"pk": 2})
    response = client.get(url)
    assert response.status_code == 404

def test_detail_template(client, db):
    post = PostFactory()
    url = reverse("detail", kwargs={"pk": post.pk})
    response = client.get(url)
    templates_found = [template.name for template in response.templates]
    assert "post_detail.html" in templates_found


def test_detail_template_content(client, db):
    post = PostFactory(title='Blog post title', body='Blog post body')
    url = reverse("detail", kwargs={"pk": post.pk})
    response = client.get(url)
    assert post.title in str(response.content)
    assert post.body in str(response.content)
