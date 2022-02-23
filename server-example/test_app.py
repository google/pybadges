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
"Tests for app"

import pytest

import app


@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client


def test_image(client):
    rv = client.get("/img?left_text=build&right_text=passing")
    assert b'build' in rv.data
    assert b'passing' in rv.data
