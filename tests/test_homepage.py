import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from movies_catalogue.main import app
from unittest.mock import Mock
import pytest

MOVIE_LIST_TYPES = [
    "popular",
    "now_playing",
    "top_rated",
    "upcoming"
]

@pytest.mark.parametrize("list_type", MOVIE_LIST_TYPES)
def test_homepage_list_types(monkeypatch, list_type):
    api_mock = Mock(return_value=[{"id": 1, "title": "Test Movie"}])

    
    monkeypatch.setattr("movies_catalogue.main.tmdb_client.get_movies_list", api_mock)

    
    monkeypatch.setattr("movies_catalogue.main.render_template", lambda *a, **kw: "DUMMY_HTML")

    with app.test_client() as client:
        response = client.get(f"/?list_type={list_type}")
        assert response.status_code == 200
        api_mock.assert_called_once_with(list_type=list_type)