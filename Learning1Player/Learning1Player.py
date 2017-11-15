"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import random

from flask import Flask, request
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

exp = {}


@app.route('/win')
def win():
    if request.args['win'] == '1':
        print("YAY!")
    else:
        print('OH WELL.')
    return ''


@app.route('/play', methods=['POST'])
def play():
    game = request.get_json()
    board = tuple(x for l in game['board'] for x in l)
    #if board in exp:
        #ret = random.
    board = tuple(x for l in reversed(game['board']) for x in l)
    ret = random.randint(1,7)
    while game['board'][ret-1][5] is not None:
        ret = random.randint(1,7)
    return str(ret)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', '127.0.0.1')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5556'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)
