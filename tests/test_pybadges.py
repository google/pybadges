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

import base64
import doctest
import json
import os.path
import unittest
import pathlib
import tempfile

import pybadges

TEST_DIR = os.path.dirname(__file__)

PNG_IMAGE_B64 = (
    'iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAD0lEQVQI12P4zw'
    'AD/xkYAA/+Af8iHnLUAAAAAElFTkSuQmCC')
PNG_IMAGE = base64.b64decode(PNG_IMAGE_B64)


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


class TestEmbedImage(unittest.TestCase):
    """Tests for pybadges._embed_image."""

    def test_data_url(self):
        url = 'data:image/png;base64,' + PNG_IMAGE_B64
        self.assertEqual(url, pybadges._embed_image(url))

    def test_http_url(self):
        url = 'https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg'
        self.assertRegex(pybadges._embed_image(url),
                         r'^data:image/svg(\+xml)?;base64,')

    def test_not_image_url(self):
        with self.assertRaisesRegex(ValueError,
                                    'expected an image, got "text"'):
            pybadges._embed_image('http://www.google.com/')

    def test_svg_file_path(self):
        image_path = os.path.abspath(
            os.path.join(TEST_DIR, 'golden-images', 'build-failure.svg'))
        self.assertRegex(pybadges._embed_image(image_path),
                         r'^data:image/svg(\+xml)?;base64,')

    def test_png_file_path(self):
        with tempfile.NamedTemporaryFile() as png:
            png.write(PNG_IMAGE)
            png.flush()
            self.assertEqual(pybadges._embed_image(png.name),
                             'data:image/png;base64,' + PNG_IMAGE_B64)

    def test_unknown_type_file_path(self):
        with tempfile.NamedTemporaryFile() as non_image:
            non_image.write(b'Hello')
            non_image.flush()
            with self.assertRaisesRegex(ValueError,
                                        'not able to determine file type'):
                pybadges._embed_image(non_image.name)

    def test_text_file_path(self):
        with tempfile.NamedTemporaryFile(suffix='.txt') as non_image:
            non_image.write(b'Hello')
            non_image.flush()
            with self.assertRaisesRegex(ValueError,
                                        'expected an image, got "text"'):
                pybadges._embed_image(non_image.name)

    def test_file_url(self):
        image_path = os.path.abspath(
            os.path.join(TEST_DIR, 'golden-images', 'build-failure.svg'))

        with self.assertRaisesRegex(ValueError, 'unsupported scheme "file"'):
            pybadges._embed_image(pathlib.Path(image_path).as_uri())


if __name__ == '__main__':
    unittest.main()
