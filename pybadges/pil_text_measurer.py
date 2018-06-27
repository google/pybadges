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

"""Measure the width, in pixels, of a string rendered using DejaVu Sans 110pt.

Uses a PIL/Pillow to determine the string length.
"""

from PIL import ImageFont

from pybadges import text_measurer


class PilMeasurer(text_measurer.TextMeasurer):
    """Measures the width of a string using PIL/Pillow."""

    def __init__(self, deja_vu_sans_path: str):
        """Initializer for PilMeasurer.

        Args:
            deja_vu_sans_path: The path to the DejaVu Sans TrueType (.ttf) font
                file.
        """
        self._font = ImageFont.truetype(deja_vu_sans_path, 110)

    def text_width(self, text: str) -> float:
        """Returns the width, in pixels, of a string in DejaVu Sans 110pt."""
        width, _ = self._font.getsize(text)
        return width
