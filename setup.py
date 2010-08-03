#!/usr/bin/python

from distutils.core import setup
import distutils.sysconfig
import os
import os.path
import re
import sys

setup(name='slingshot',
      version='0.9',
      description='Simple 2D shooting strategy game set in space, with gravity',
      author='See README',
      license='GNU General Public License version 2, or (at your option) ' +\
              'any later version',
      scripts=['src/slingshot.py'],
      packages=['slingshot'],
      package_data={'slingshot':['data/*.png',
                                 'data/*.ttf']},
      package_dir={'slingshot':'src/slingshot'},
#      cmdclass={'build_path':build_path}
)
