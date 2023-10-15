from Flask import flask
from threading import Thread

app = flask.Flask('app')

@app.route('/')
def main():
    return 'xxx'

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run())
    server.start()