#!/usr/bin/env python3

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

import argparse
import json
import os
import os.path
import pkg_resources

import pybadges

def generate_images(source_json_path, target_directory):
    os.makedirs(target_directory, exist_ok=True)
    with open(source_json_path) as f:
        examples = json.load(f)

    for example in examples:
        filename = os.path.join(target_directory, example.pop('file_name'))
        with open(filename, 'w') as f:
            f.write(pybadges.badge(**example))


def main():
    parser = argparse.ArgumentParser(description='generate a github-style badge given some text and colors')

    parser.add_argument('--source-path',
                        default=pkg_resources.resource_filename(__name__, 'tests/test-badges.json'),
                        help='the text to show on the left-hand-side of the badge')

    parser.add_argument('--destination-dir',
                        default=pkg_resources.resource_filename(__name__, 'tests/golden-images'),
                        help='the text to show on the left-hand-side of the badge')
    args = parser.parse_args()
    generate_images(args.source_path, args.destination_dir)


if __name__ == '__main__':
    main()
