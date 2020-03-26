#!/usr/bin/env python3
# Copyright (C) 2010 Ryan Kavanagh <ryanakca@kubuntu.org>
#
# Slingshot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Slingshot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Slingshot; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA


from distutils.core import setup
import distutils.sysconfig
import os
import os.path
import re
import sys

# Default prefix
prefix = '/usr/local'
# Get the install prefix if one is specified from the command line
for i, arg in enumerate(sys.argv):
    prefix_regex = re.compile('(?P<prefix>--prefix)?[\=\s]?(?P<path>/[\w\s/]*)')
    if prefix_regex.match(arg):
        if prefix_regex.match(arg).group('prefix') and not prefix_regex.match(arg).group('path'):
            # We got --prefix with a space instead of an equal. The next arg will have our path.
            prefix = os.path.expandvars(prefix_regex.match(sys.argv[i+1]).group('path'))
        elif prefix_regex.match(arg).group('path'):
            prefix = prefix_regex.match(arg).group('path')
        elif (sys.argv[i-1] == '--prefix') and prefix_regex.match(arg).group('path'):
            prefix = os.path.expandvars(prefix_regex.match(arg).group('path'))

data_files = [(os.path.join(prefix,'share/applications/'),
                    ['data/slingshot.desktop']),
              (os.path.join(prefix, 'share/pixmaps/'),
                    ['data/slingshot.xpm'])
            ]

setup(name='slingshot',
      version='0.9',
      description='Simple 2D shooting strategy game set in space, with gravity',
      author='See README',
      license='GNU General Public License version 2, or (at your option) ' +\
              'any later version',
      scripts=['src/bin/slingshot'],
      packages=['slingshot'],
      package_data={'slingshot':['data/*.png',
                                 'data/*.ttf']},
      package_dir={'slingshot':'src/slingshot'},
      data_files=data_files,
)
