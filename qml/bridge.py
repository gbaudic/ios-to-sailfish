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
import re
import logging
import sys
from pathlib import Path
try:
    import pyotherside
except ImportError:
    pyotherside = None
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ios-backup-core', 'src'))
from ios_backup_core.backup import BackupReader, LocalBackupAccessor, open_local_backup
from ios_backup_core.extractors.photos import PhotoExtractor
from ios_backup_core.extractors.podcasts import podcasts_to_opml
from ios_backup_core.extractors.calendar_events import events_to_ics

reader = None
accessor = None
home = Path.home()
notes = dict()
photos = dict()
events = dict()
calls = dict()
contacts = dict()
podcasts = dict()
loyalty = dict()
messages = dict()
voicemail = dict()
voice_memos = dict()
docs = dict()
backup_dir = ""


def open_backup(path, password=None):
    global reader, accessor, backup_dir
    try:
        backup_dir = path
        accessor = open_local_backup(path, password)
        reader = BackupReader(accessor)
    except ValueError as e:
        msg = e.args[0]
        if 'Not a valid backup' in msg:
            pyotherside.send('not-a-backup')
        elif 'Backup is encrypted' in msg:
            pyotherside.send('encrypted-backup')
        elif 'Failed to decrypt' in msg:
            pyotherside.send('decryption-error')
        
    pass


def export_notes(dry_run=False):
    global notes
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
    global podcasts
    if dry_run:
        podcasts = reader.podcasts()
        pyotherside.send('analysis-complete', 'podcasts', len(podcasts['podcasts']))
    else:
        opml = podcasts_to_opml(podcasts['podcasts'])
        with open(os.path.join(home, 'Downloads'), 'w') as f:
            f.write(opml)
        pyotherside.send('migration-progress', 'podcasts', len(podcasts['podcasts']))


def export_calendar(dry_run=False):
    global events
    pass


def export_loyalty(dry_run=False):
    global loyalty
    pass


def migrate_call_history(dry_run=False):
    global calls
    if dry_run:
        calls = reader.calls()
        pyotherside.send('analysis-complete', 'calls', calls['total'])
    else:
        # read everything
        calls = reader.calls(offset=0, limit=calls['total'])
        pass


def migrate_contacts(dry_run=False):
    global contacts
    if dry_run:
        contacts = reader.contacts()
        pyotherside.send('analysis-complete', 'contacts', len(contacts['contacts']))
    pass


def migrate_messages(dry_run=False):
    global messages
    if dry_run:
        messages = reader.messages()
    pass


def migrate_pictures_and_videos(dry_run=False):
    global photos, backup_dir
    if dry_run:
        media_extractor = PhotoExtractor()
        photos = media_extractor.list_photos(accessor)
        pyotherside.send('analysis-complete', 'media', photos['total'])
    else:
        i = 0
        for media in photos['photos']:
            source_path = os.path.join(backup_dir, media['file_hash'][:2], media['file_hash'])

            destination_path = os.path.join(home,
                'Movies' if media['kind'] == 'video' else 'Pictures',
                'Camera',
                media['filename']
            )

            shutil.copy2(source_path, destination_path)
            i += 1
            pyotherside.send('migration-progress', 'media', i)


def migrate_user_docs(dry_run=False):
    global docs, backup_dir
    pass


def export_voice_memos(dry_run=False):
    global voice_memos, backup_dir
    pass


def export_voicemail(dry_run=False):
    global voicemail
    if dry_run:
        voicemail = reader.voicemail()
        pyotherside.send('analysis-complete', 'voicemail', len(voicemail['voicemails']))
    pass


def migrate(migrations, dry_run=False):
    """ Parent function to call specific migrations """
    if dry_run:
        migrate_call_history(dry_run)
        migrate_contacts(dry_run)
        migrate_messages(dry_run)
        export_notes(dry_run)
        migrate_pictures_and_videos(dry_run)
        migrate_user_docs(dry_run)
        export_calendar(dry_run)
        export_loyalty(dry_run)
        export_podcasts(dry_run)
        export_voice_memos(dry_run)
        export_voicemail(dry_run)
    else:
        # Only migrate what is in the migrations list
        pass
    pass


if __name__ == '__main__':
    global backup_dir
    backup_dir = sys.argv[1]
    migrate([], True)
    pass
