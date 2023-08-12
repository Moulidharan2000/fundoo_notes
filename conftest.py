import pytest
from rest_framework.reverse import reverse


@pytest.fixture()
def user_register(django_user_model, client):
    data = {
        "first_name": "Harish",
        "last_name": "kumar",
        "username": "harik",
        "password": "hark2000",
        "email": "harishkumar@gmail.com",
        "phone_num": 9632587410,
        "location": "Mumbai"
    }
    url = reverse("create")
    response = client.post(url, data, content_type="application/json")
    return response.data["data"]["id"]


@pytest.fixture()
def get_token(user_register, client):
    data = {
        "username": "harik",
        "password": "hark2000"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    return {"content_type": "application/json", "HTTP_TOKEN": response.data["token"]}


@pytest.fixture()
def create_note(user_register, client, get_token):
    data = {
        "title": "qwer",
        "description": "3rfjafqw",
        "remainder": "2023-07-31T17:32:00Z"
    }
    url = reverse("notes")
    response = client.post(url, data, **get_token)
    return response.data


@pytest.fixture()
def set_is_archive(create_note, client, get_token):
    data = {
        "id": create_note["data"]["id"]
    }
    url = reverse("archived")
    response = client.post(url, data, **get_token)
    return response.data


@pytest.fixture()
def set_is_trash(create_note, client, get_token):
    data = {
        "id": create_note["data"]["id"]
    }
    url = reverse("trash")
    response = client.post(url, data, **get_token)
    return response.data


@pytest.fixture()
def create_label(client, get_token):
    data = {
        "name": "notes2",
        "user": 1,
        "color": "blue",
        "font": "sample"
    }
    url = reverse("labels")
    response = client.post(url, data, **get_token)
    return response.data


@pytest.fixture()
def collaborators(client):
    data = {
        "first_name": "Harish",
        "last_name": "kumar",
        "username": "raj",
        "password": "hark2000",
        "email": "harishkumar@gmail.com",
        "phone_num": 9632587410,
        "location": "Mumbai"
    }
    url = reverse("create")
    response = client.post(url, data, content_type="application/json")
    return response.data["data"]["id"]


@pytest.fixture()
def label_collaborators(client, get_token):
    data = {
        "name": "kfkja",
        "user": 2,
        "color": "blue",
        "font": "sample"
    }
    url = reverse("labels")
    response = client.post(url, data, **get_token)
    return response.data["data"]["id"]
