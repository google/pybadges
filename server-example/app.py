# Copyright 2020 The pybadge Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Example Flask server that serves badges."""

import flask
import pybadges

app = flask.Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """Serve an HTML page containing badge images."""
    badges = [
        {
            'left_text': 'Build',
            'right_text': 'passing',
            'left_color': '#555',
            'right_color': '#008000'
        },
        {
            'left_text': 'Build',
            'right_text': 'fail',
            'left_color': '#555',
            'right_color': '#800000'
        },
        {
            "left_text":
                "complete",
            "right_text":
                "example",
            "left_color":
                "green",
            "right_color":
                "yellow",
            "logo":
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAD0lEQVQI12P4zwAD/xkYAA/+Af8iHnLUAAAAAElFTkSuQmCC"
        },
    ]
    for b in badges:
        b['url'] = flask.url_for('.serve_badge', **b)
    return flask.render_template('index.html', badges=badges)


@app.route('/img')
def serve_badge():
    """Serve a badge image based on the request query string."""
    badge = pybadges.badge(left_text=flask.request.args.get('left_text'),
                           right_text=flask.request.args.get('right_text'),
                           left_color=flask.request.args.get('left_color'),
                           right_color=flask.request.args.get('right_color'),
                           logo=flask.request.args.get('logo'))

    response = flask.make_response(badge)
    response.content_type = 'image/svg+xml'
    return response


if __name__ == '__main__':
    app.run()
