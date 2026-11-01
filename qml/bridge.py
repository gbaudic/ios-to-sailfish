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

import os
import shutil
import pyotherside
from pathlib import Path
from ios_backup_core import BackupReader
from ios_backup_core.extractors.photos import PhotoExtractor

reader = None
home = Path.home()
notes = dict()
photos = dict()
backup_dir = ""

def open_backup(path, password=None):
    try:
        backup_dir = path
        reader = BackupReader.from_path(path, password)
    except ValueError as e:
        msg = e.args[0]
        if 'Not a valid backup' in msg:
            pyotherside.send('not-a-backup')
        elif 'Backup is encrypted' in msg:
            pyotherside.send('encrypted-backup')
        elif 'Failed to decrypt' in msg:
            pyotherside.send('decryption-error')
        
    pass

def migrate_notes(dry_run=False):
    if dry_run:
        notes = reader.notes()
        pyotherside.send('analysis-complete', 'notes', len(notes['notes']))
    else:
        i = 0
        for note in notes['notes']:
            with open(os.path.join(home, 'Documents', note['note_id']), 'w') as f:
                f.write(note['body'])
            i += 1
            pyotherside.send('migration-progress', 'notes', i)
    
def export_podcasts(dry_run=False):
    pass

def export_calendar(dry_run=False):
    pass

def export_loyalty(dry_run=False):
    pass

def migrate_call_history(dry_run=False):
    calls = reader.calls()
    pass

def migrate_contacts(dry_run=False):
    contacts = reader.contacts()
    pyotherside.send('analysis-complete', 'contacts', len(contacts['contacts']))
    pass

def migrate_messages(dry_run=False):
    messages = reader.messages()
    pass

def migrate_pictures_and_videos(dry_run=False):
    if dry_run:
        media_extractor = PhotoExtractor()
        photos = media_extractor.list_photos(reader._accessor)
        pyotherside.send('analysis-complete', 'media', photos['total']))
    else:
        i = 0
        for media in photos['photos']:
            source_path = os.path.join(self.backup_dir, media['file_hash'][:2], media['file_hash'])

            destination_path = os.path.join(home,
                'Movies' if media['kind'] == 'video' else 'Pictures',
                'Camera',
                media['filename']
            )

            shutil.copy2(source_path, destination_path)
            i += 1
            pyotherside.send('migration-progress', 'media', i)


def migrate_user_docs(dry_run=False):
    pass

def migrate(migrations, dry_run=False):
    """ Parent function to call specific migrations """
    if dry_run:
        migrate_call_history(dry_run)
        migrate_contacts(dry_run)
        migrate_messages(dry_run)
        migrate_notes(dry_run)
        migrate_pictures_and_videos(dry_run)
        migrate_user_docs(dry_run)
        export_calendar(dry_run)
        export_loyalty(dry_run)
        export_podcasts(dry_run)
    else:
        # Only migrate what is in the migrations list
        pass
    pass

