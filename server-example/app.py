# Copyright 2018 The pybadge Authors
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

""" Example CI server that serves badges """

from flask import Flask
import pybadges

app = Flask(__name__)


@app.route('/')
def serveBadges():
    # First example
    badge_arg = dict(
        left_text='build',
        right_text='passing',
        right_color='#008000')
    badge = pybadges.badge(**badge_arg)

    # Second example
    secondBadge = pybadges.badge('chat', 'online')
    return badge + "\n" + secondBadge


if __name__ == '__main__':
    app.run()
