import pytest
from flask import Flask


@pytest.fixture()
def flask_app():
    app = Flask(__name__)
    app.secret_key = "test-key"
    # Import here to ensure app context is isolated per test
    from controllers.auth_controller import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app


def test_login_page_get(flask_app):
    client = flask_app.test_client()
    resp = client.get("/auth/login")
    assert resp.status_code == 200


def test_login_redirects_on_failure(monkeypatch, flask_app):
    # Force login_user to return None
    import controllers.auth_controller as auth_controller

    monkeypatch.setattr(auth_controller, "login_user", lambda e, p: None)
    client = flask_app.test_client()
    resp = client.post("/auth/login", data={"email": "x", "password": "y"})
    assert resp.status_code in (301, 302)


def test_dashboard_requires_login(flask_app):
    client = flask_app.test_client()
    resp = client.get("/auth/dashboard")
    assert resp.status_code in (301, 302)
