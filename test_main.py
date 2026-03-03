
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db, Base
from main import Candidate

# Create Test Database (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_candidates.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


# --------------------------
# FIXTURE: Database Session
# --------------------------

@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# --------------------------
# FIXTURE: Test Client
# --------------------------

@pytest.fixture()
def client(db):

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


# --------------------------
# TEST: Create Candidate
# --------------------------

def test_create_candidate(client):
    response = client.post("/candidates", json={
        "name": "Jaswanth",
        "email": "jaswanth@test.com",
        "phone": "9876543210",
        "maths_marks": 80,
        "history_marks": 70
    })

    assert response.status_code == 200
    assert response.json()["email"] == "jaswanth@test.com"


# --------------------------
# TEST: Duplicate Email
# --------------------------

def test_duplicate_email(client):

    data = {
        "name": "Test",
        "email": "duplicate@test.com",
        "phone": "9876543211",
        "maths_marks": 50,
        "history_marks": 60
    }

    client.post("/candidates", json=data)
    response = client.post("/candidates", json=data)

    assert response.status_code == 400
    assert "Email already exists" in response.text


# --------------------------
# TEST: Get Candidates
# --------------------------

def test_get_candidates(client):
    response = client.get("/candidates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --------------------------
# TEST: Update Candidate
# --------------------------

def test_update_candidate(client):
    create = client.post("/candidates", json={
        "name": "Old Name",
        "email": "update@test.com",
        "phone": "9876543212",
        "maths_marks": 40,
        "history_marks": 40
    })

    candidate_id = create.json()["id"]

    response = client.put(
        f"/candidates/{candidate_id}",
        json={"name": "New Name"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


# --------------------------
# TEST: Delete Candidate
# --------------------------

def test_delete_candidate(client):
    create = client.post("/candidates", json={
        "name": "Delete Me",
        "email": "delete@test.com",
        "phone": "9876543213",
        "maths_marks": 60,
        "history_marks": 60
    })

    candidate_id = create.json()["id"]

    response = client.delete(f"/candidates/{candidate_id}")
    assert response.status_code == 200
    assert "Deleted Successfully" in response.text
