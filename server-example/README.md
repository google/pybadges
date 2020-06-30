## Simple Flask Server

This is a simple example of how a
[Flask](https://flask.palletsprojects.com/) server can serve badges.

### Installing

Before running the server, you must install Flask and pybadges. You can install both with:

```sh
pip install -r requirements.txt
```

### Running

To run the server, you must set the FLASK_APP environment variable before running the server using Flask:

```sh
export FLASK_APP=app.py
flask run
```

After this step, you can view your badge on http://127.0.0.1:5000/
