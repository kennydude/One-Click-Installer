#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Joe Simpson headangerkenny@googlemail.com
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys

try:
    import DistUtilsExtra.auto
except ImportError:
    print >> sys.stderr, 'To build project_name you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'


def update_config(values = {}):

    oldvalues = {}
    try:
        fin = file('one_click_installer_lib/one_click_installerconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find one_click_installer_lib/one_click_installerconfig.py")
        sys.exit(1)
    return oldvalues


def update_desktop_file(datadir):

    try:
        fin = file('one-click-installer.desktop.in', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find one-click-installer.desktop.in")
        sys.exit(1)


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'__one-click-installer_data_directory__': "'%s'" % (self.prefix + '/share/one-click-installer/'),
                  '__version__': "'%s'" % self.distribution.get_version()}
        previous_values = update_config(values)
        update_desktop_file(self.prefix + '/share/project_name/')
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)


        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='one-click-installer',
    version='0.1-public1',
    license='GPL-3',
    author='Joe Simpson',
    author_email='headbangerkenny@googlemail.com',
    url='https://launchpad.net/one-click-installer',
    data_files=[('/usr/share/mime/packages', ['one-click-installer.xml'])],
    description='Easy PPA installation!',
    long_description='Easy PPA installation! This allows you to quickly add PPAs and packages without having to fiddle around with silly command line prompts, which can be dangerous!',
    cmdclass={'install': InstallAndUpdateDataDirectory}
    )

