
import base64


def auth():
    encoded = base64.b64encode(
        b"test-admin:test-long-password"
    ).decode()

    return {
        "Authorization": f"Basic {encoded}"
    }


def test_liveness_without_credentials(client):
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_requires_admin(client):
    response = client.get("/")

    assert response.status_code == 401

    response = client.get(
        "/",
        headers=auth(),
    )

    assert response.status_code == 200
    assert "JobScout AI" in response.text


def test_profile_requires_admin(client):
    response = client.get("/api/v1/profile")

    assert response.status_code == 401


def test_profile_rejects_invalid_radius_without_database(
    client,
):
    response = client.put(
        "/api/v1/profile",
        headers=auth(),
        json={
            "locations": [
                {
                    "city": "Munich",
                    "radius_km": -4,
                }
            ]
        },
    )

    assert response.status_code == 422


def test_wrong_credentials_rejected(client):
    response = client.get(
        "/",
        headers={
            "Authorization": "Basic bm86bm8="
        },
    )

    assert response.status_code == 401
