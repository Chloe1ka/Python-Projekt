"""Integrationstests für /mitglieder."""

from http import HTTPStatus
from typing import Final
from uuid import uuid4

import anyio
import pytest
from httpx import ASGITransport, AsyncClient, Response

from python_projekt import app
from python_projekt.db import SessionLocal
from python_projekt.models import Mitglied

_SEED_IDS: Final = frozenset({1, 2})


def _call(method: str, url: str, json: dict[str, str] | None = None) -> Response:
    async def send() -> Response:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as http:
            return await http.request(method, url, json=json)

    return anyio.run(send)


class _Client:
    def get(self, url: str) -> Response:
        return _call("GET", url)

    def post(self, url: str, json: dict[str, str]) -> Response:
        return _call("POST", url, json=json)


@pytest.fixture
def client() -> _Client:
    return _Client()


def _delete_mitglied(mitglied_id: int) -> None:
    if mitglied_id in _SEED_IDS:
        return
    db = SessionLocal()
    try:
        mitglied = db.get(Mitglied, mitglied_id)
        if mitglied is None:
            return
        db.delete(mitglied)
        db.commit()
    finally:
        db.close()


def test_get_mitglieder(client: _Client) -> None:
    # act
    response: Final = client.get("/mitglieder")

    # assert
    assert response.status_code == HTTPStatus.OK
    body: Final = response.json()
    assert isinstance(body, list)


def test_get_mitglied_by_id(client: _Client) -> None:
    # act
    response: Final = client.get("/mitglieder/1")

    # assert
    assert response.status_code == HTTPStatus.OK
    body: Final = response.json()
    assert isinstance(body, dict)
    assert body.get("id") == 1
    assert body.get("vorname") is not None
    assert body.get("nachname") is not None
    assert body.get("email") is not None
    assert body.get("version") is not None


def test_post_mitglied(client: _Client) -> None:
    # arrange
    email: Final = f"test.{uuid4()}@example.com"
    neues_mitglied: Final = {
        "vorname": "Tina",
        "nachname": "Test",
        "email": email,
    }
    created_id: int | None = None

    try:
        # act
        response: Final = client.post("/mitglieder", json=neues_mitglied)

        # assert
        assert response.status_code == HTTPStatus.CREATED
        body: Final = response.json()
        assert isinstance(body, dict)
        raw_id = body.get("id")
        if isinstance(raw_id, int):
            created_id = raw_id
        assert body.get("vorname") == "Tina"
        assert body.get("nachname") == "Test"
        assert body.get("email") == email
        assert isinstance(body.get("id"), int)
        assert isinstance(body.get("version"), int)
    finally:
        if created_id is not None:
            _delete_mitglied(created_id)


def test_post_mitglied_ohne_email(client: _Client) -> None:
    # arrange
    unvollstaendig: Final = {"vorname": "Tina", "nachname": "Test"}

    # act
    response: Final = client.post("/mitglieder", json=unvollstaendig)

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
