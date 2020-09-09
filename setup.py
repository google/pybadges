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
"""A setup module for pybadges."""

import base64
import re

from setuptools import setup


def get_long_description():
    """Transform README.md into a usable long description.

    Replaces relative references to svg images to absolute https references.
    """

    with open('README.md') as f:
        read_me = f.read()

    def replace_relative_with_absolute(match):
        svg_path = match.group(0)[1:-1]
        return ('(https://github.com/google/pybadges/raw/master/'
                '%s?sanitize=true)' % svg_path)

    return re.sub(r'\(tests/golden-images/.*?\.svg\)',
                  replace_relative_with_absolute, read_me)


setup(
    name='pybadges',
    version='2.3.0',  # Also change in version.py.
    author='Brian Quinlan',
    author_email='brian@sweetapp.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    description='A library and command-line tool for generating Github-style ' +
    'badges',
    keywords="github gh-badges badge shield status",
    package_data={
        'pybadges': [
            'badge-template-full.svg', 'default-widths.json', 'py.typed'
        ]
    },
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    python_requires='>=3.4',
    install_requires=['Jinja2>=2.9.0,<3', 'requests>=2.9.0,<3'],
    extras_require={
        'pil-measurement': ['Pillow>=5,<6'],
        'trend': ['drawsvg>=1.6.0', 'numpy>=1.19.0'],
        'dev': [
            'fonttools>=3.26', 'nox', 'Pillow>=5', 'pytest>=3.6', 'xmldiff>=2.4'
        ],
    },
    license='Apache-2.0',
    packages=["pybadges"],
    url='https://github.com/google/pybadges')
