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
# Logic coming from https://github.com/soyersoyer/ios-sms-export-to-sailfish, no licence provided

import sqlite3
import json
import os
import extractor
import logging

logger = logging.getLogger()

class SMSExporter(extractor.Extractor):
    ''' Exporter for SMS data (and only SMS) '''
    
    def get_db_source(self):
        return "3d0d7e5fb2ce288813306e4d4636395e047a3d28"
    
    def apply(self):
        conn = sqlite3.connect(self.get_absolute_db_source(), detect_types=sqlite3.PARSE_COLNAMES)
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        cursor = conn.cursor()

        cursor.execute('SELECT rowid as handle_id, id as `to`, "sms" as type FROM handle')
        handles = []
        for handle in cursor.fetchall():
            cursor.execute("""SELECT
                strftime('%Y-%m-%dT%H:%M:%fZ', substr(date, 1, 9) + 978307200, 'unixepoch') as `date`,
                case when is_from_me = 0 then "in" else "out" end as direction,
                text
                from message
                where handle_id = ?""",
                (handle['handle_id'],))
            handle['messages'] = cursor.fetchall()
            if len(handle['messages']):
                handles.append(handle)

        with open(os.path.join(self.output_dir, "sms.json"), 'w') as outfile:
            json.dump(handles, outfile, indent=4)


