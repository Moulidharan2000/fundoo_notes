from rest_framework.reverse import reverse


def test_user_registration_success(django_user_model, client):
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
    assert response.status_code == 201


def test_user_registration_failure(django_user_model, client):
    data = {
        "first_name": "Harish",
        "last_name": "kumar",
        "username": "$#54587",
        "password": "hark2000",
        "email": "harishkumar@gmail.com",
        "phone_num": 9632587410,
        "location": "Mumbai"
    }
    url = reverse("create")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 400


def test_user_login_success(django_user_model, client, user_register):
    data = {
        "username": "harik",
        "password": "hark2000"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200


def test_user_login_failure(django_user_model, client, user_register):
    data = {
        "username": "harisk",
        "password": "hark2000"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 400
