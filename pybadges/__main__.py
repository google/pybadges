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

"""Output a github-style badge as an SVG image given some text and colors.

For more information, run:
$ python3 -m pybadges --help
"""

import argparse
import sys
import tempfile
import webbrowser

import pybadges


def main():
    parser = argparse.ArgumentParser(
        description='generate a github-style badge given some text and colors')

    parser.add_argument(
        '--left-text',
        default='license',
        help='the text to show on the left-hand-side of the badge')
    parser.add_argument(
        '--right-text',
        default='APACHE',
        help='the text to show on the right-hand-side of the badge')
    parser.add_argument(
        '--whole-link',
        default=None,
        help='the url to redirect to when the badge is clicked')
    parser.add_argument(
        '--left-link',
        default=None,
        help='the url to redirect to when the left-hand of the badge is ' +
             'clicked')
    parser.add_argument(
        '--right-link',
        default=None,
        help='the url to redirect to when the right-hand of the badge is ' +
             'clicked')
    parser.add_argument(
        '--left-color',
        default='#555',
        help='the background color of the left-hand-side of the badge')
    parser.add_argument(
        '--right-color',
        default='#007ec6',
        help='the background color of the right-hand-side of the badge')
    parser.add_argument(
        '--logo',
        default=None,
        help='a URI reference to a logo to display in the badge')
    parser.add_argument(
        '--browser',
        action='store_true',
        default=False,
        help='display the badge in a browser tab')
    parser.add_argument(
        '--use-pil-text-measurer',
        action='store_true',
        default=False,
        help='use the PilMeasurer to measure the length of text (kerning may '
             'be more precise for non-Western languages. ' +
             '--deja-vu-sans-path must also be set.')
    parser.add_argument(
        '--deja-vu-sans-path',
        default=None,
        help='the path to the ttf font file containing DejaVu Sans. If not ' +
             'present on your system, you can download it from ' +
             'https://www.fontsquirrel.com/fonts/dejavu-sans')

    args = parser.parse_args()

    if (args.left_link or args.right_link) and args.whole_link:
        print(
            'argument --whole-link: cannot be set with ' +
            '--left-link or --right-link',
            file=sys.stderr)
        sys.exit(1)

    measurer = None
    if args.use_pil_text_measurer:
        if args.deja_vu_sans_path is None:
            print(
                'argument --use-pil-text-measurer: must also set ' +
                '--deja-vu-sans-path',
                file=sys.stderr)
            sys.exit(1)
        from pybadges import pil_text_measurer
        measurer = pil_text_measurer.PilMeasurer(args.deja_vu_sans_path)

    badge = pybadges.badge(left_text=args.left_text, right_text=args.right_text,
                           left_link=args.left_link, right_link=args.right_link,
                           whole_link=args.whole_link,
                           left_color=args.left_color,
                           right_color=args.right_color,
                           logo=args.logo,
                           measurer=measurer)

    if args.browser:
        _, badge_path = tempfile.mkstemp(suffix='.svg')
        with open(badge_path, 'w') as f:
            f.write(badge)

        webbrowser.open_new_tab('file://' + badge_path)
    else:
        print(badge, end='')


main()
