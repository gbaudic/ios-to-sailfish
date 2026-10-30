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

import pyotherside
from ios_backup_core import BackupReader
from ios_backup_core.extractors.photos import PhotoExtractor, VIDEO_EXTENSIONS

reader = None

def open_backup(path, password=None):
    try:
        reader = BackupReader.from_path(path, password)
    except ValueError as e:
        msg = e.args[0]
        if 'Not a valid backup' in msg:
            pyotherside.send('not-a-backup')
        elif 'Backup is encrypted' in msg:
            pyotherside.send('encrypted-backup')
        elif 'Failed to decrypt' in msg:
            pyotherside.send('wrong-password')
        
    pass

def migrate_notes():
    notes = reader.notes()
    pass
    
def export_podcasts():
    pass

def export_calendar():
    pass

def export_loyalty():
    pass

def migrate_call_history():
    calls = reader.calls()
    pass

def migrate_contacts():
    contacts = reader.contacts()
    pass

def migrate_messages():
    messages = reader.messages()
    pass

def migrate_pictures_and_videos():
    extractor = PhotoExtractor()
    pass

def migrate_user_docs():
    pass

def migrate(**kwargs):
    """ Parent function to call specific migrations """
    pass

