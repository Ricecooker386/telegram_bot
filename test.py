import logging
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return 'hi'

if __name__ == '__main__':
    app.run(host='0.0.0.0')