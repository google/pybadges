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

"""Nox config for running lint and unit tests."""

import nox


@nox.session
def lint(session):
    """Run flake8.
    Returns a failure if flake8 finds linting errors or sufficiently
    serious code quality issues.
    """
    session.install('flake8')
    session.run('flake8',
                'pypadges,tests')


@nox.session(python=['3.4', '3.5', '3.6', '3.7'])
@nox.parametrize('pip_installs',
                 [[], ['Jinja2==2.9.0', 'Pillow==5.0.0', 'requests==2.9.0']])
def unit(session, pip_installs):
    """Run the unit test suite."""

    session.install('-e', '.[dev]')
    for package in pip_installs:
        session.install(package)

    session.run(
        'py.test',
        '--quiet',
        'tests',
        *session.posargs
    )
