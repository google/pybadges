## Simple Server

### Installing

Before running, it is **recommended** to install the versions of packages that were used when writing this code:

```sh
pip install -r requirements.txt
```

And if you don't have installed flask yet:

```sh
apt install python3-flask
```

### Running

You must inform the environment variable FLASK_APP and then run:

```sh
export FLASK_APP=hello.py
flask run
```

 * Running on http://127.0.0.1:5000/