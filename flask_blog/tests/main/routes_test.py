

# -------------------
# Home Page Test
# -------------------
def test_index(client):
    """
        Tests GET request for home page.
        Confirms the route loads and contains "Home Page" in HTML.

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home Page' in response.data


# -------------------
# About Page Test
# -------------------
def test_about(client):
    """
        Tests GET request for about page.
        Confirms the route loads and contains "About Page" in HTML.

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
    """
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Page' in response.data