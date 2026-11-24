from itertools import count
from fastapi.testclient import TestClient
import pytest
from main import app
import main

client = TestClient(app)

fake_list = [
    {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and vegetables for the week",
        "completed": False,
        "id": 1,
    },
    {
        "title": "Finish project report",
        "description": "Complete the quarterly summary and send it to the team",
        "completed": True,
        "id": 2,
    },
    {
        "title": "Schedule dentist appointment",
        "description": "Book a cleaning for next month",
        "completed": False,
        "id": 4,
    },
    {
        "title": "Review pull request",
        "description": "Check the authentication changes in the login module",
        "completed": False,
        "id": 6,
    },
    {
        "title": "Update README",
        "description": "Replace the outdated setup steps with uv instructions",
        "completed": False,
        "id": 7,
    },
    {
        "title": "Plan weekend trip",
        "description": "Look up train times and book a place to stay",
        "completed": False,
        "id": 8,
    },
]


@pytest.fixture(autouse=True)
def reset_state():
    """Give every test a clean in-memory store and ID counter."""
    main.tasks.clear()
    main.counter = count(start=1)
    yield
    main.tasks.clear()
    main.counter = count(start=1)


def test_get_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == main.tasks


def test_get_with_data():
    main.tasks = list(fake_list)
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == main.tasks


def test_get_id_invalid_id():
    main.tasks = list(fake_list)
    response = client.get("/tasks/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_get_id_valid_id():
    main.tasks = list(fake_list)
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == fake_list[0]


@pytest.mark.parametrize("title", ["", "   ", "\n\t"])
def test_post_invalid(title):
    response = client.post(
        "/tasks",
        json={
            "title": title,
            "description": "There goes my stealer",
            "completed": True,
        },
    )

    assert response.status_code == 422
    assert response.json() == {"detail": "Title can't be empty"}


def test_post_invalid_bool():
    response = client.post(
        "/tasks",
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread, and vegetables for the week",
            "completed": "tr",
        },
    )
    assert response.status_code == 422


def test_post():
    response = client.post(
        "/tasks",
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread, and vegetables for the week",
            "completed": True,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and vegetables for the week",
        "completed": True,
        "id": 1,
    }


def test_delete_doesnt_repeat_id():
    for i in range(10):
        response = client.post(
            "/tasks",
            json={
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and vegetables for the week",
                "completed": True,
            },
        )
        assert response.status_code == 201

    response = client.delete("/tasks/10")
    assert response.status_code == 204

    response = client.delete("/tasks/5")
    assert response.status_code == 204

    response = client.post(
        "/tasks",
        json={
            "title": "New record",
            "description": "new description",
            "completed": True,
        },
    )
    assert response.status_code == 201

    for task in main.tasks:
        assert task["id"] not in (5, 10)


def test_update_doesnt_modify_other():
    for i in range(10):
        response = client.post(
            "/tasks",
            json={
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and vegetables for the week",
                "completed": True,
            },
        )
        assert response.status_code == 201

    response = client.put(
        "/tasks/5",
        json={
            "title": "Updated title",
            "description": "Updated desc",
            "completed": True,
        },
    )
    assert response.status_code == 200
    assert response.json() == main.tasks[4]

    for task in main.tasks:
        if task["id"] != 5 and (
            task["title"] == "Updated title" or task["description"] == "Updated desc"
        ):
            assert False
        assert True


def test_unique_id():
    ids = []
    for i in range(100):
        response = client.post(
            "/tasks",
            json={
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and vegetables for the week",
                "completed": True,
            },
        )
        assert response.status_code == 201

    for task in main.tasks:
        ids.append(task["id"])
    assert len(ids) == len(set(ids))


def test_deletion_gives_404():
    for i in range(10):
        response = client.post(
            "/tasks",
            json={
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and vegetables for the week",
                "completed": True,
            },
        )
        assert response.status_code == 201

    response = client.delete("/tasks/10")
    assert response.status_code == 204

    response = client.get("/tasks/10")
    assert response.status_code == 404

    response = client.get("/tasks/10")
    assert response.status_code == 404


@pytest.mark.parametrize("title", ["", "   ", "\n\t"])
def test_put_invalid_title(title):
    response = client.post(
        "/tasks",
        json={
            "title": "title",
            "description": "There goes my stealer",
            "completed": True,
        },
    )
    assert response.status_code == 201
    response = client.put(
        "/tasks/1",
        json={
            "title": title,
            "description": "There goes my stealer",
            "completed": True,
        },
    )

    assert response.status_code == 422
    assert response.json() == {"detail": "Title can't be empty"}


def test_put():
    response = client.post(
        "/tasks",
        json={
            "title": "title",
            "description": "Milk, eggs, bread, and vegetables for the week",
            "completed": True,
        },
    )
    assert response.status_code == 201
    response = client.put(
        "/tasks/1",
        json={
            "title": "hello",
            "description": "There goes my stealer",
            "completed": True,
        },
    )
    assert response.status_code == 200


def test_put_invalid():
    response = client.post(
        "/tasks",
        json={
            "title": "title",
            "description": "Milk, eggs, bread, and vegetables for the week",
            "completed": True,
        },
    )
    assert response.status_code == 201
    response = client.put(
        "/tasks/2",
        json={
            "title": "hello",
            "description": "There goes my stealer",
            "completed": True,
        },
    )
    assert response.status_code == 404


def test_delete_invalid():
    response = client.post(
        "/tasks",
        json={
            "title": "title",
            "description": "Milk, eggs, bread, and vegetables for the week",
            "completed": True,
        },
    )
    assert response.status_code == 201
    response = client.delete("/tasks/2")
    assert response.status_code == 404


def test_delete_valid():
    response = client.post(
        "/tasks",
        json={
            "title": "title",
            "description": "Milk, eggs, bread, and vegetables for the week",
            "completed": True,
        },
    )
    assert response.status_code == 201
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    assert main.tasks == []


def test_get_with_id_string():
    main.tasks = list(fake_list)
    response = client.get("/tasks/abc")
    assert response.status_code == 422
