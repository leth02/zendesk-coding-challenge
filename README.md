# Ticket Viewer Application | zendesk-coding-challenge
This is an application to view support tickets from my Zendesk account. What this application does is:
- [x] Connect to the Zendesk API
- [x] Request all the tickets for my account
- [x] Display the tickets in a table (page through tickets if more than 25 ones are returned)
- [x] Display individual ticket details

## Install and run the application
This project expects you to have Python (Python 3 preferred) on your machine. You can follow the instructions here to install Python if your machine does not have it: https://www.python.org/downloads/

**1. Clone the project to your machine**
```
$ git clone https://github.com/leth02/zendesk-coding-challenge.git
$ cd zendesk-coding-challenge
```
**2. Create and activate a virtual environment (recommended)**
```
$ python -m venv venv
$ . venv/bin/activate
```

**3. Install required packages**
```
$ python -m pip install -r requirements.txt
```

**4. Set the API token for Zendesk API Authentication**

In order to use the API from Zendesk, you need an API token. Please contact me to request one.
After obtaining an API token, you can set it as an environment variable with the following command:

```
$ export API_TOKEN={the_api_token}
```

**5. Set up Flask and start the application**
```
$ export FLASK_APP=ticket_viewer_app
$ export FLASK_ENV=development
$ flask run
```

**6. Navigate to http://127.0.0.1:5000/ on your browser and start using the application**

## Test the application
You can run tests using pytest. It will run all of the unit and functional tests.
```
$ python -m pytest
```

