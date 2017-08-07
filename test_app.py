import pytest
import json
from flask import url_for
from app import app as _app
from app import db, Widget


@pytest.fixture
def app():
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    _app.config["TESTING"] = True
    _app.config["SERVER_NAME"] = "test_server"
    with _app.app_context():
        db.create_all()
        w = Widget(name="one", color="r")
        db.session.add(w)
        db.session.commit()
    return _app


def test_graphql_names(app):
    query = """
    {
      widgets {
        edges {
          node {
            name
          }
        }
      }
    }
    """
    with app.app_context():
        url = url_for('graphql', query=query)

    client = app.test_client()
    resp = client.get(url)
    assert resp.status_code == 200
    result = json.loads(resp.data.decode())
    assert result == {
      "data": {
        "widgets": {
          "edges": [{
            "node": {
              "name": "one"
            }
          }]
        }
      }
    }


def test_graphql_colors(app):
    query = """
    {
      widgets {
        edges {
          node {
            color
          }
        }
      }
    }
    """
    with app.app_context():
        url = url_for('graphql', query=query)

    client = app.test_client()
    resp = client.get(url)
    assert resp.status_code == 200
    result = json.loads(resp.data.decode())
    assert result == {
      "data": {
        "widgets": {
          "edges": [{
            "node": {
              "color": "r"
            }
          }]
        }
      }
    }
