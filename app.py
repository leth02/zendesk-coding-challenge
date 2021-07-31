from flask import Flask, jsonify, request, render_template, redirect, url_for
from requests import post, get
from urllib.parse import urlencode
import base64

API_TOKEN = "ERQExBDWQQpUBusqJIa5aA3RNdUHgqKNnabHH64O"
HOST = "https://zcctanthole.zendesk.com"

def get_authorization_header():
    credentials = "leth02@luther.edu/token:{api_token}".format(api_token=API_TOKEN)
    return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")


app = Flask(__name__)


# ========== Views ==========
@app.route('/', methods=["GET"])
def main():
    return render_template('index.html')


@app.route('/api/tickets/get')
def get_tickets():
    url = HOST + "/api/v2/tickets.json"
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

    url = HOST + "/api/v2/search.json?" + urlencode(params)
    print(url)
    headers = {"Authorization": "Basic {}".format(get_authorization_header())}
    response = get(url, headers=headers)
    results = response.json()
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8998)