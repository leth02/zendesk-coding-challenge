from flask import Flask, jsonify, request, render_template
from requests import get
from urllib.parse import urlencode
from base64 import b64encode


def create_app(test_config=None):
    """Create and configure an instance of the Ticket Viewer Flask application."""
    app = Flask(__name__)

    # default configuration for the app
    app.config.from_mapping(
        SECRET_KEY='zcc_tanthole_dev',
        API_TOKEN='ERQExBDWQQpUBusqJIa5aA3RNdUHgqKNnabHH64O',
        ZENDESK_HOST='https://zcctanthole.zendesk.com'
    )

    # if the test config is passed, use it
    if test_config:
        app.config.update(test_config)

    # ========== Helper functions ==========
    def get_authorization_header():
        credentials = 'leth02@luther.edu/token:{api_token}'.format(api_token=app.config['API_TOKEN'])
        return b64encode(credentials.encode('utf-8')).decode('utf-8')


    # ========== Views ==========
    @app.route('/', methods=["GET"])
    def main():
        return render_template('index.html')


    # ========== APIs ==========
    @app.route('/api/tickets/get')
    def get_tickets():
        url = app.config['ZENDESK_HOST'] + "/api/v2/tickets.json"
        headers = {"Authorization": "Basic {}".format(get_authorization_header())}
        response = get(url, headers=headers)
        results = response.json()
        return jsonify(results), 200


    @app.route('/api/search', methods=["POST"])
    def search():
        search_string = request.json.get('search_string', '')
        params = {
            'query': search_string
        }

        url = app.config['ZENDESK_HOST'] + "/api/v2/search.json?" + urlencode(params)
        print(url)
        headers = {"Authorization": "Basic {}".format(get_authorization_header())}
        response = get(url, headers=headers)
        results = response.json()
        return jsonify(results), 200


    return app
