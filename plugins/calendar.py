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

import sqlite3
import logging
import os
from extractor import Extractor

logger = logging.getLogger()

class Calendar(Extractor):
    ''' Exporter for calendar events '''
    
    def get_db_source(self):
        return "2041457d5fe04d39d0ab481178355df6781e6858"
    
    def apply(self):
        
        conn = sqlite3.connect(self.get_absolute_db_source())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        events = list()
        try:
            cursor.execute("""SELECT
                    summary as SUMMARY, 
                    location_id, 
                    strftime('%Y%m%dT%H%M%SZ', substr(start_date, 1, 9) + 978307200, 'unixepoch') as DTSTART, 
                    start_tz,
                    strftime('%Y%m%dT%H%M%SZ', substr(end_date, 1, 9) + 978307200, 'unixepoch') as DTEND, 
                    end_tz,
                    all_day,
                    calendar_id,
                    unique_identifier as UID
                FROM CalendarItem
            """)

            for row in cursor.fetchall():
                event = dict()
                event['UID'] = row['UID']
                event['DTSTART'] = row['DTSTART']
                event['DTEND'] = row['DTEND']
                event['DTSTAMP'] = row['DTSTART']
                event['SUMMARY'] = row['SUMMARY']
                event['DESCRIPTION'] = ''
                
                # Fetch location if any
                if row['location_id'] != 0:
                    cursor.execute('SELECT title as LOCATION from Location where ROWID = ?',(row['location_id'],))
                    for location in cursor.fetchall():
                        event['LOCATION'] = location['LOCATION']
                
                events.append(event)

        finally:
            conn.close()
        
        if events:
            with open(os.path.join(self.output_dir, 'Events.ics'), 'w', encoding='utf-8') as fp:
                fp.write("BEGIN:VCALENDAR\n")
                fp.write("VERSION:2.0\n")
                for event in events:
                    fp.write("BEGIN:VEVENT\n")
                    for key, value in event.items():
                        fp.write(f"{key}:{value}\n")
                    fp.write("END:VEVENT\n")
                fp.write("END:VCALENDAR")

