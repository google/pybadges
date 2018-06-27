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

"""Creates a github-style badge as a SVG image.

This package seeks to generate semantically-identical output to the JavaScript
gh-badges library
(https://github.com/badges/shields/blob/master/doc/gh-badges.md)

>>> badge(left_text='coverage', right_text='23%', right_color='red')
'<svg...</svg>'
>>> badge(left_text='build', right_text='green', right_color='green',
...       whole_link="http://www.example.com/")
'<svg...</svg>'
>>> # base64-encoded PNG image
>>> image_data = 'iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAD0lEQVQI12P4zwAD/xkYAA/+Af8iHnLUAAAAAElFTkSuQmCC'
>>> badge(left_text='build', right_text='green', right_color='green',
...       logo="data:image/png;base64," + image_data)
'<svg...</svg>'
"""

import jinja2
from typing import Optional
from xml.dom import minidom

from pybadges import text_measurer
from pybadges import precalculated_text_measurer


_JINJA2_ENVIRONMENT = jinja2.Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=jinja2.PackageLoader('pybadges', '.'),
    autoescape=jinja2.select_autoescape(['svg']))

# Use the same color scheme as describe in:
# https://github.com/badges/shields/blob/master/lib/colorscheme.json

_NAME_TO_COLOR = {
    'brightgreen': '#4c1',
    'green': '#97CA00',
    'yellow': '#dfb317',
    'yellowgreen': '#a4a61d',
    'orange': '#fe7d37',
    'red': '#e05d44',
    'blue': '#007ec6',
    'grey': '#555',
    'gray': '#555',
    'lightgrey': '#9f9f9f',
    'lightgray': '#9f9f9f',
}


def _remove_blanks(node):
    for x in node.childNodes:
        if x.nodeType == minidom.Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == minidom.Node.ELEMENT_NODE:
            _remove_blanks(x)


def badge(left_text: str, right_text: str, left_link: Optional[str] = None,
          right_link: Optional[str] = None,
          whole_link: Optional[str] = None, logo: Optional[str] = None,
          left_color: str = '#555', right_color: str = '#007ec6',
          measurer: Optional[text_measurer.TextMeasurer] = None) -> str:
    """Creates a github-style badge as an SVG image.

    >>> badge(left_text='coverage', right_text='23%', right_color='red')
    '<svg...</svg>'
    >>> badge(left_text='build', right_text='green', right_color='green',
    ...       whole_link="http://www.example.com/")
    '<svg...</svg>'

    Args:
        left_text: The text that should appear on the left-hand-side of the
            badge e.g. "coverage".
        right_text: The text that should appear on the right-hand-side of the
            badge e.g. "23%".
        left_link: The URL that should be redirected to when the left-hand text
            is selected.
        right_link: The URL that should be redirected to when the right-hand
            text is selected.
        whole_link: The link that should be redirected to when the badge is
            selected. If set then left_link and right_right may not be set.
        logo: A url representing a logo that will be displayed inside the
            badge. Can be a data URL e.g. "data:image/svg+xml;utf8,<svg..."
        left_color: The color of the part of the badge containing the left-hand
            text. Can be an valid CSS color
            (see https://developer.mozilla.org/en-US/docs/Web/CSS/color) or a
            color name defined here:
            https://github.com/badges/shields/blob/master/lib/colorscheme.json
        right_color: The color of the part of the badge containing the
            right-hand text. Can be an valid CSS color
            (see https://developer.mozilla.org/en-US/docs/Web/CSS/color) or a
            color name defined here:
            https://github.com/badges/shields/blob/master/lib/colorscheme.json
        measurer: A text_measurer.TextMeasurer that can be used to measure the
            width of left_text and right_text.

    """
    if measurer is None:
        measurer = (
            precalculated_text_measurer.PrecalculatedTextMeasurer
                .default())

    if (left_link or right_link) and whole_link:
        raise ValueError(
            'whole_link may not bet set with left_link or right_link')
    template = _JINJA2_ENVIRONMENT.get_template('badge-template-full.svg')
    svg = template.render(
        left_text=left_text,
        right_text=right_text,
        left_text_width=measurer.text_width(left_text) / 10.0,
        right_text_width=measurer.text_width(right_text) / 10.0,
        left_link=left_link,
        right_link=right_link,
        whole_link=whole_link,
        logo=logo,
        left_color=_NAME_TO_COLOR.get(left_color, left_color),
        right_color=_NAME_TO_COLOR.get(right_color, right_color),
    )
    xml = minidom.parseString(svg)
    _remove_blanks(xml)
    xml.normalize()
    return xml.documentElement.toxml()
