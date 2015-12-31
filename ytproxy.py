#!/usr/bin/env python

"""
Simple Youtube streaming proxy

Usage:

1. Run `pip install flask`,
2. Install youtube-dl (try: `sudo apt-get install youtube-dl`),
3. Run `python ytproxy.py`,
4. Point your browser to http://localhost:5000
"""

from flask import Flask, Response, request, stream_with_context
import subprocess
app = Flask(__name__)


@app.route("/ytdl")
def hello():

    def streamGenerator():
        p = subprocess.Popen(['youtube-dl', request.args['url'], '-o', '-'],
                             stdout=subprocess.PIPE)
        while True:
            y = p.stdout.read(1024)
            if y != '':
                yield y

    resp = stream_with_context(streamGenerator())
    return Response(resp, mimetype='video/webm')


@app.route("/")
def index():
    return 'Enter YT URL: <form action=/ytdl><input name=url />'

if __name__ == "__main__":
    app.run()
