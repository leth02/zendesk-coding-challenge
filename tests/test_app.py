from ticket_viewer_app import create_app
from pytest import fixture
from unittest.mock import patch


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_requests_get_tickets(*args, **kwargs):
    return MockResponse({"count": 100, "tickets": []}, 200)


def mock_requests_get_tickets_fails_404(*args, **kwargs):
    return MockResponse({"error": "Failed to get tickets. Please try again later."}, 404)


class TestTicketViewerApp:
    @fixture
    def client(self):
        flask_app = create_app({"TESTING": True})
        
        with flask_app.test_client() as test_client:
            with flask_app.app_context():
                yield test_client

    
    def test_main_page_should_pass(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Ticket Viewer App | Zendesk Coding Challenge - Tan Tho Le' in response.data


    def test_main_page_should_fail_with_unallowed_method(self, client):
        response = client.post('/')
        assert response.status_code == 405
        assert b'Ticket Viewer App | Zendesk Coding Challenge - Tan Tho Le' not in response.data


    @patch('requests.get', side_effect=mock_requests_get_tickets)
    def test_get_tickets_should_pass(self, request, client):
        response = client.get('/api/tickets/get')
        assert isinstance(response.json['count'], int)
        assert isinstance(response.json['tickets'], list)

    @patch('requests.get', side_effect=mock_requests_get_tickets_fails_404)
    def test_get_tickets_fails_with_404(self, request, client):
        response = client.get('/api/tickets/get')
        assert response.status_code == 404
        assert response.json['error'] == "Failed to get tickets. Please try again later."
