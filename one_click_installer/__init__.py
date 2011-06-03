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

import optparse

import gettext, sys, logging
from gettext import gettext as _
gettext.textdomain('one-click-installer')

import gtk

from one_click_installer import OneClickInstallerWindow

from one_click_installer_lib import set_up_logging, preferences, get_version

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs one_click_installer_lib also)"))
    (options, args) = parser.parse_args()
        
    if len(args) != 1:
        print "You must launch the application with a .oneclickinstaller file!"
        sys.exit()
    to_open = args[0]

    set_up_logging(options)
    print("Going to open file '%s' when the UI has launched. Please wait" % to_open)    
    return to_open

def main():
    'constructor for your class instances'
    to_open = parse_options()

    # Run the application.    
    window = OneClickInstallerWindow.OneClickInstallerWindow()
    window.show()
    window.set_file(to_open)
    gtk.gdk.threads_init() 
    gtk.main()
