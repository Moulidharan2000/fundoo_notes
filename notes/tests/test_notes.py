import token
from rest_framework.reverse import reverse
import pytest


@pytest.mark.django_db
def test_create_note_success(client, get_token):
    data = {
        "title": "qwer",
        "description": "3rfjafqw",
        "remainder": "2023-07-31T17:32:00Z"
    }
    url = reverse("notes")
    response = client.post(url, data, **get_token)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_note_failure(client, get_token):
    data = {
        "title": "#adafa",
        "description": "3#rfjafqw",
        "remainder": "segsg"
    }
    url = reverse("notes")
    response = client.post(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_notes_success(client, get_token, create_note):
    url = reverse("notes")
    response = client.get(url, create_note, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_notes_failure(client, get_token, create_note):
    url = reverse("notes")
    response = client.get(url, create_note)
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_note_success(client, get_token, create_note):
    data = {
        "id": create_note["data"]["id"],
        "title": "ma124bx",
        "description": "oiuaqtqt1e",
        "remainder": "2023-07-31T17:34:00Z"
    }
    url = reverse("notes")
    response = client.put(url, data, **get_token)
    assert response.status_code == 200
    assert response.data["data"]["title"] == "ma124bx"


@pytest.mark.django_db
def test_update_note_failure(client, get_token, create_note):
    data = {
        "id": 45,
        "title": "ma124bx",
        "description": "oiuaqtqt1e",
        "remainder": "2023-07-31T17:34:00Z"
    }
    url = reverse("notes")
    response = client.put(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_note_success(client, create_note, get_token):
    data = {
        "id": create_note["data"]["id"]
    }
    url = reverse("notes")
    response = client.delete(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_note_failure(client, create_note, get_token):
    data = {
        "id": 4
    }
    url = reverse("notes")
    response = client.delete(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_isarchive_success(client, create_note, get_token):
    data = {
        "id": create_note["data"]["id"]
    }
    url = reverse("archived")
    response = client.post(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_isarchive_failure(client, create_note, get_token):
    data = {
        "id": 4
    }
    url = reverse("archived")
    response = client.post(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_isarchive_success(client, set_is_archive, get_token):
    url = reverse("archived")
    response = client.get(url, set_is_archive, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_isarchive_failure(client, set_is_archive, get_token):
    url = reverse("archived")
    response = client.get(url, set_is_archive)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_istrash_success(client, create_note, get_token):
    data = {
        "id": create_note["data"]["id"]
    }
    url = reverse("trash")
    response = client.post(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_istrash_failure(client, create_note, get_token):
    data = {
        "id": 45
    }
    url = reverse("trash")
    response = client.post(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_istrash_success(client, set_is_trash, get_token):
    url = reverse("trash")
    response = client.get(url, set_is_trash, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_istrash_failure(client, set_is_trash):
    url = reverse("trash")
    response = client.get(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_collaborator_success(client, user_register, collaborators, create_note, get_token):
    data = {
        "id": create_note["data"]["id"],
        "collaborators": [collaborators]
    }
    url = reverse("collaborator")
    response = client.post(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_collaborator_failure(client, user_register, collaborators, create_note, get_token):
    data = {
        "id": 56,
        "collaborators": [collaborators]
    }
    url = reverse("collaborator")
    response = client.post(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_collaborator_success(client, user_register, create_note, collaborators, get_token):
    data = {
        "id": create_note["data"]["id"],
        "collaborators": [collaborators]
    }
    url = reverse("collaborator")
    response = client.delete(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_collaborator_failure(client, user_register, create_note, collaborators, get_token):
    data = {
        "id": 85,
        "collaborators": [collaborators]
    }
    url = reverse("collaborator")
    response = client.delete(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_label_success(client, get_token):
    data = {
        "name": "notes2",
        "user": 1,
        "color": "blue",
        "font": "sample"
    }
    url = reverse("labels")
    response = client.post(url, data, **get_token)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_label_failure(client, get_token):
    data = {
        "name": "yfyh98",
        "user": 1,
        "color": "blue",
        "font": "sample"
    }
    url = reverse("labels")
    response = client.post(url, **get_token)
    print(response.data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_label_success(client, create_label, get_token):
    data = {
        "id": 1,
    }
    url = reverse("labels")
    response = client.get(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_label_failure(client, create_label, get_token):
    data = {
        "id": 5
    }
    url = reverse("labels")
    response = client.get(url, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_label_success(client, create_label, get_token):
    data = {
        "id": create_label["data"]["id"],
        "name": "notes1",
        "color": "red",
        "font": "timesnewroman",
        "user": 2
    }
    url = reverse("labels")
    response = client.put(url, data, **get_token)
    assert response.status_code == 200
    assert response.data["data"]["name"] == "notes1"


@pytest.mark.django_db
def test_put_label_failure(client, create_label, get_token):
    data = {
        "id": 50,
        "name": "notes1",
        "color": "red",
        "font": "timesnewroman",
        "user": 2
    }
    url = reverse("labels")
    response = client.put(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_label_success(client, create_label, get_token):
    data = {
        "id": create_label["data"]["id"]
    }
    url = reverse("labels")
    response = client.delete(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_label_failure(client, create_label, get_token):
    data = {
        "id": 4
    }
    url = reverse("labels")
    response = client.delete(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_labelcollaborator_success(client, user_register, create_note, create_label, label_collaborators,
                                        get_token):
    data = {
        "id": create_label["data"]["id"],
        "labels": [label_collaborators]
    }
    url = reverse("label_notes")
    response = client.post(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_labelcollaborator_failure(client, user_register, create_note, create_label, label_collaborators,
                                        get_token):
    data = {
        "id": 5,
        "labels": [label_collaborators]
    }
    url = reverse("label_notes")
    response = client.post(url, data, **get_token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_labelcollaborator_success(client, user_register, create_note, create_label, label_collaborators,
                                          get_token):
    data = {
        "id": create_label["data"]["id"],
        "labels": [label_collaborators]
    }
    url = reverse("label_notes")
    response = client.post(url, data, **get_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_labelcollaborator_failure(client, user_register, create_note, create_label, label_collaborators,
                                          get_token):
    data = {
        "id": 10,
        "labels": [label_collaborators]
    }
    url = reverse("label_notes")
    response = client.post(url, data, **get_token)
    assert response.status_code == 400
