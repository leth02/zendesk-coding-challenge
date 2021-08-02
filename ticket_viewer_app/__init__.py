from flask import Flask, jsonify, request, render_template
import requests
from urllib.parse import urlencode
from base64 import b64encode
import os
from dotenv import load_dotenv
load_dotenv()


def create_app(test_config=None):
    """Create and configure an instance of the Ticket Viewer Flask application."""
    app = Flask(__name__)

    # default configuration for the app
    app.config.from_mapping(
        SECRET_KEY='zcc_tanthole_dev',
        API_TOKEN=os.environ['API_TOKEN'],
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
    @app.route('/api/tickets/get', methods=["GET"])
    def get_tickets():
        url = app.config['ZENDESK_HOST'] + "/api/v2/tickets.json"
        headers = {"Authorization": "Basic {}".format(get_authorization_header())}
        response = requests.get(url, headers=headers)
        
        # Return a friendly message if the request fails
        if response.status_code != 200:
            return jsonify({"error": "Failed to get tickets. Please try again later."}), 404

        results = response.json()
        return jsonify(results), 200


    @app.route('/api/search', methods=["POST"])
    def search():
        search_string = request.json.get('search_string', '')
        params = {
            'query': search_string
        }

        url = app.config['ZENDESK_HOST'] + "/api/v2/search.json?" + urlencode(params)
        headers = {"Authorization": "Basic {}".format(get_authorization_header())}
        response = requests.get(url, headers=headers)

        # Return an error message if the request fails 
        if response.status_code != 200:
            return jsonify({"error": "Failed to search against the provided query string."}), 404

        results = response.json()
        return jsonify(results), 200


    return app
