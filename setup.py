#!/usr/bin/env python

from distutils.core import setup
from distutils.errors import DistutilsArgError

from setuptools.command.install import install

import os
import subprocess
import sys
import time
import pip

from pip.commands.show import search_packages_info

class MyInstall(install):
    def run(self):
        # Anything that can cause a failure must happen before install.run().
        # If install.run() completes successfully, pip will always return that
        # the installation succeeded.

        if "win32" != sys.platform:
            raise Exception("Windows is the only supported platform")

        # install_requires/dependency_links doesn't work because the wheel
        # wouldn't be installed until install.run(self). This is a bad plan
        # because pywin32_postinstall can't run until the wheel is installed,
        # if this is after install.run(self) then we can't return failures
        # properly.
        pkgs = list(search_packages_info(["pywin32"]))
        if len(pkgs) > 1:
            raise Exception("error: multiple pywin32 detected")
        elif len(pkgs) == 1:
            pywin32 = pkgs[0]
            assert pywin32['name'] == 'pywin32'
            if pywin32['version'] != '220':
                raise Exception("error: incompatible version of pywin32 installed: {}".format(pywin32['version']))
        else:
            assert len(pkgs) == 0
            # wheel lifted from here http://www.lfd.uci.edu/~gohlke/pythonlibs/
            wheel = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pywin32-220-cp27-none-win32.whl")
            pip.main(['install', wheel])

        rootdir     = os.path.dirname(os.path.realpath(__file__))
        postinstall = os.path.join(rootdir, "pywin32_postinstall.py")
        subprocess.check_call([sys.executable, postinstall, "-install"])

        install.run(self)

setup(name='pywin32-wrapper',
      version='1.0',
      description='Handle installation intricacies for pywin32',
      author='Aaron Burrow',
      author_email='burrows@preveil.com',
      url='https://github.com/PreVeil/pywin32-wrapper',
      packages=[],
      cmdclass={'install': MyInstall},
     )
