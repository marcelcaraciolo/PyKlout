#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) - 2011 Marcel Pinheiro Caraciolo  <marcel @orygens.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup
import pyklout

name = "pyklout"

version = str(pyklout.__version__)


setup(name=name,
      version=version,
      description="Python Wrapper for Klout (http://klout.com/) API",
      author="Marcel Caraciolo",
      author_email='caraciol@gmail.com',
      long_description="""
      Python interface for Klout (http://klout.com/) API
      """,
      url="https://github.com/marcelcaraciolo/PyKlout",
      download_url='https://github.com/marcelcaraciolo/PyKlout/tarball/master',
      license="LGPL3",
      keywords="klout api",
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Topic :: Utilities",
                   "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2",
                   "Topic :: Internet",
                   "Topic :: Internet :: WWW/HTTP",
                   ],
      py_modules=['pyklout', 'test_klout'],
)
