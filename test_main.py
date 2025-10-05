
import pytest
from unittest.mock import Mock
from movies_catalogue.main import app

MOVIE_LIST_TYPES = ["popular", "now_playing", "top_rated", "upcoming"]

@pytest.mark.parametrize("list_type", MOVIE_LIST_TYPES)
def test_homepage(monkeypatch, list_type):
    """Testuje stronę główną Flask dla różnych typów list filmów."""
    mock_movies = [{"id": 1, "title": "Test Movie"}]

    # Mock API TMDB
    api_mock = Mock(return_value=mock_movies)
    monkeypatch.setattr("movies_catalogue.tmdb_client.get_movies_list", api_mock)

    # Mock render_template (nie ładujemy HTML)
    monkeypatch.setattr("movies_catalogue.main.render_template", lambda *a, **kw: "DUMMY_HTML")

    with app.test_client() as client:
        response = client.get(f"/?list_type={list_type}")
        assert response.status_code == 200
        api_mock.assert_called_once_with(list_type=list_type)
