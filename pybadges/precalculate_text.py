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

"""Creates a JSON file that can be used by precalculated_text_measurer.py.

Creates a JSON file that can be used by
precalculated_test_measurer.PrecalculatedTextMeasurer to calculate the pixel
length of text strings rendered in DejaVu Sans font.

The output JSON object is formatted like:
{
    'mean-character-length': <float: the average pixel length of a character in
                              DejaVu Sans at 110pt>,
    'character-lengths': <Map[str, float]: a mapping between single characters
                          and their length in DejaVu Sans at 110pt>,
    'kerning-characters': <str: a string containing all of the characters that
                           kerning information is available for>,
    'kerning-pairs': <Map[str, float]: a mapping between pairs of characters
                      (e.g. "IJ") to the amount of kerning distance between
                      them. Positive values are *subtracted* from the string
                      length e.g. text-length-of("IJ") =>
                            (character-lengths["I"] + character-lengths["J"]
                            - kerning-pairs["IJ"])
                      If two characters both appear in 'kerning-characters' but
                      don't have an entry in 'kerning-pairs' then the kerning
                      distance between them is zero.
}

For information about the commands, run:
$ python3 - m pybadges.precalculate_text --help
"""

import argparse
import itertools
import json
import os.path
import statistics
from typing import Iterable, Mapping, TextIO

from fontTools import ttLib

from pybadges import pil_text_measurer
from pybadges import text_measurer


def generate_supported_characters(deja_vu_sans_path: str) -> Iterable[str]:
    """Generate the characters support by the font at the given path."""
    font = ttLib.TTFont(deja_vu_sans_path)
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            for code in cmap.cmap:
                yield chr(code)


def generate_encodeable_characters(characters: Iterable[str],
                                   encodings: Iterable[str]) -> Iterable[str]:
    """Generates the subset of 'characters' that can be encoded by 'encodings'.

    Args:
        characters: The characters to check for encodeability e.g. 'abcd'.
        encodings: The encodings to check against e.g. ['cp1252', 'iso-8859-5'].

    Returns:
        The subset of 'characters' that can be encoded using one of the provided
        encodings.
    """
    for c in characters:
        for encoding in encodings:
            try:
                c.encode(encoding)
                yield c
            except UnicodeEncodeError:
                pass


def calculate_character_to_length_mapping(
        measurer: text_measurer.TextMeasurer,
        characters: Iterable[str]) -> Mapping[str, float]:
    """Return a mapping between each given character and its length.

    Args:
        measurer: The TextMeasurer used to measure the width of the text in
            pixels.
        characters: The characters to measure e.g. "ml".

    Returns:
        A mapping from the given characters to their length in pixels, as
        determined by 'measurer' e.g. {'m': 5.2, 'l', 1.2}.
    """
    char_to_length = {}

    for c in characters:
        char_to_length[c] = measurer.text_width(c)
    return char_to_length


def calculate_pair_to_kern_mapping(
        measurer: text_measurer.TextMeasurer,
        char_to_length: Mapping[str, float],
        characters: Iterable[str]) -> Mapping[str, float]:
    """Returns a mapping between each *pair* of characters and their kerning.

    Args:
        measurer: The TextMeasurer used to measure the width of each pair of
            characters.
        char_to_length: A mapping between characters and their length in pixels.
            Must contain every character in 'characters' e.g.
            {'h': 5.2, 'e': 4.0, 'l', 1.2, 'o': 5.0}.
        characters: The characters to generate the kerning mapping for e.g.
            'hel'.

    Returns:
        A mapping between each pair of given characters
        (e.g. 'hh', he', hl', 'eh', 'ee', 'el', 'lh, 'le', 'll') and the kerning
        adjustment for that pair of characters i.e. the difference between the
        length of the two characters calculated using 'char_to_length' vs.
        the length calculated by `measurer`. Positive values indicate that the
        length is less than using the sum of 'char_to_length'. Zero values are
        excluded from the map e.g. {'hl': 3.1, 'ee': -0.5}.
    """
    pair_to_kerning = {}
    for a, b in itertools.permutations(characters, 2):
        kerned_width = measurer.text_width(a + b)
        unkerned_width = char_to_length[a] + char_to_length[b]
        kerning = unkerned_width - kerned_width
        if abs(kerning) > 0.05:
            pair_to_kerning[a + b] = round(kerning, 3)
    return pair_to_kerning


def write_json(f: TextIO, deja_vu_sans_path: str,
               measurer: text_measurer.TextMeasurer,
               encodings: Iterable[str]) -> None:
    """Write the data required by PrecalculatedTextMeasurer to a stream."""
    supported_characters = list(
        generate_supported_characters(deja_vu_sans_path))
    kerning_characters = ''.join(
        generate_encodeable_characters(supported_characters, encodings))
    char_to_length = calculate_character_to_length_mapping(measurer,
                                                           supported_characters)
    pair_to_kerning = calculate_pair_to_kern_mapping(measurer, char_to_length,
                                                     kerning_characters)
    json.dump(
        {'mean-character-length': statistics.mean(char_to_length.values()),
         'character-lengths': char_to_length,
         'kerning-characters': kerning_characters,
         'kerning-pairs': pair_to_kerning},
        f, sort_keys=True, indent=1)


def main():
    parser = argparse.ArgumentParser(
        description='generate a github-style badge given some text and colors')

    parser.add_argument(
        '--deja-vu-sans-path',
        required=True,
        help='the path to the ttf font file containing DejaVu Sans. If not ' +
             'present on your system, you can download it from ' +
             'https://www.fontsquirrel.com/fonts/dejavu-sans')

    parser.add_argument(
        '--kerning-pair-encodings',
        action='append',
        default=['cp1252'],
        help='only include kerning pairs for the given encodings')

    parser.add_argument(
        '--output-json-file',
        default=os.path.join(os.path.dirname(__file__),
                             'default-widths.json'),
        help='the path where the generated JSON will be placed. If the ' +
             'provided filename extension ends with .xz then the output' +
             'will be compressed using lzma.')

    args = parser.parse_args()

    measurer = pil_text_measurer.PilMeasurer(args.deja_vu_sans_path)

    def create_file():
        if args.output_json_file.endswith('.xz'):
            import lzma
            return lzma.open(args.output_json_file, 'wt')
        else:
            return open(args.output_json_file, 'wt')

    with create_file() as f:
        write_json(
            f, args.deja_vu_sans_path, measurer, args.kerning_pair_encodings)


if __name__ == '__main__':
    main()
