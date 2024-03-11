from django.urls import reverse
from .conftest import post_factory, test_user
from .models import Post


def test_home_status_code(client, db):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


def test_home_greeting_user(client, db, test_user):
    client.force_login(test_user)
    url = reverse("home")
    response = client.get(url)
    assert f"Hi {test_user.username}!" in response.content.decode()


def test_home_unauthenticated_user(client, db):
    url = reverse("home")
    response = client.get(url)
    assert "You are not logged in." in response.content.decode()


def test_home_template(client, db):
    url = reverse("home")
    response = client.get(url)
    templates_found = [template.name for template in response.templates]
    assert "home.html" in templates_found


def test_home_template_content(client, db, post_factory):
    url = reverse("home")
    response = client.get(url)
    assert "Django Blog" in str(response.content)
    assert post_factory.title in str(response.content)
    assert post_factory.body in str(response.content)


def test_detail_status_code(client, db, post_factory):
    url = reverse("detail", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    assert response.status_code == 200


def test_detail_unexisting_post(client, db, post_factory):
    url = reverse("detail", kwargs={"pk": 2})
    response = client.get(url)
    assert response.status_code == 404


def test_detail_template(client, db, post_factory):
    url = reverse("detail", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    templates_found = [template.name for template in response.templates]
    assert "post_detail.html" in templates_found


def test_detail_template_content(client, db, post_factory):
    url = reverse("detail", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    assert post_factory.title in str(response.content)
    assert post_factory.body in str(response.content)


def test_post_new_status_code(client, db):
    url = reverse("post_new")
    response = client.get(url)
    assert response.status_code == 200


def test_post_new_template(client, db):
    url = reverse("post_new")
    response = client.get(url)
    templates_found = [template.name for template in response.templates]
    assert "post_new.html" in templates_found


def test_post_new_template_content(client, db):
    url = reverse("post_new")
    response = client.get(url)
    assert "New Blog Post" in str(response.content)


def test_post_new_creates_post(client, db, test_user):
    client.force_login(test_user)
    url = reverse("post_new")
    response = client.post(
        url, {"title": "Test title", "body": "Test body", "author": test_user.pk}
    )
    assert response.status_code == 302
    assert Post.objects.count() == 1
    post = Post.objects.first()
    assert post.title == "Test title"
    assert post.body == "Test body"


def test_post_edit_status_code(client, db, post_factory):
    url = reverse("post_edit", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    assert response.status_code == 200


def test_post_edit_template(client, db, post_factory):
    url = reverse("post_edit", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    templates_found = [template.name for template in response.templates]
    assert "post_edit.html" in templates_found


def test_post_edit_template_content(client, db, post_factory):
    url = reverse("post_edit", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    assert "Edit Blog Post" in str(response.content)


def test_post_edit_can_edit_post(client, db, test_user, post_factory):
    client.force_login(test_user)
    url = reverse("post_edit", kwargs={"pk": post_factory.pk})
    response = client.post(
        url, {"title": "Edited title", "body": "Edited body", "author": test_user.pk}
    )
    assert response.status_code == 302
    assert Post.objects.count() == 1
    post = Post.objects.first()
    assert post.title == "Edited title"
    assert post.body == "Edited body"


def test_post_delete_status_code(client, db, post_factory):
    url = reverse("post_delete", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    assert response.status_code == 200


def test_post_delete_template(client, db, post_factory):
    url = reverse("post_delete", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    templates_found = [template.name for template in response.templates]
    assert "post_delete.html" in templates_found


def test_post_delete_template_content(client, db, post_factory):
    url = reverse("post_delete", kwargs={"pk": post_factory.pk})
    response = client.get(url)
    assert "Delete Blog Post" in str(response.content)


def test_post_delete_deletes_post(client, db, test_user, post_factory):
    client.force_login(test_user)
    url = reverse("post_delete", kwargs={"pk": post_factory.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert Post.objects.count() == 0
