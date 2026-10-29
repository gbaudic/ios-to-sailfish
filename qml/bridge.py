# -*- coding: utf-8 -*-
#
# ios-to-sailfish - A collection of Python scripts to easily migrate from iOS to SailfishOS
# Copyright (c) 2026 G. Baudic
#
# ios-to-sailfish is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# ios-to-sailfish is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import platform

backup_version = '1.0'
ui_version = '0.1'

def python_version():
    return platform.python_version()

def plugin_version():
    pass

def migrate_notes():
    pass
    
def export_podcasts():
    pass

def export_calendar():
    pass

def export_loyalty():
    pass

def migrate_call_history():
    pass

def migrate_contacts():
    pass

def migrate_messages():
    pass

def migrate_pictures_and_videos():
    pass

def migrate_user_docs():
    pass

def migrate(**kwargs):
    """ Parent function to call specific migrations """
    pass

