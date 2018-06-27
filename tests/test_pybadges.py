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

"""Tests for pybadges."""

import doctest
import json
import os.path
import unittest

import pybadges

TEST_DIR = os.path.dirname(__file__)


class TestPybadgesBadge(unittest.TestCase):
    """Tests for pybadges.badge."""

    def test_docs(self):
        doctest.testmod(pybadges, optionflags=doctest.ELLIPSIS)

    def test_whole_link_and_left_link(self):
        with self.assertRaises(ValueError):
            pybadges.badge(left_text='foo', right_text='bar',
                           left_link='http://example.com/',
                           whole_link='http://example.com/')

    def test_changes(self):
        with open(os.path.join(TEST_DIR, 'test-badges.json'), 'r') as f:
            examples = json.load(f)

        for example in examples:
            file_name = example.pop('file_name')
            with self.subTest(example=file_name):
                filepath = os.path.join(TEST_DIR, 'golden-images', file_name)

                with open(filepath, 'r') as f:
                    golden_image = f.read()
                pybadge_image = pybadges.badge(**example)
                self.assertEqual(golden_image, pybadge_image)


if __name__ == '__main__':
    unittest.main()
