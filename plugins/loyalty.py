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
import json
import os
import time
from extractor import Extractor
import logging

logger = logging.getLogger()

class Fira2Sailcards(Extractor):
    ''' Exporter for Fira loyalty cards to Sailcards backup format '''
    
    def get_db_source(self):
        return "9f2ebf21c85d2cb89efc4ff3ef527bb5b8e36774"
    
    def apply(self):
        conn = sqlite3.connect(self.get_absolute_db_source())
        conn.row_factory = sqlite3.Row
        
        handles = dict()
        handles["cards"] = list()
        handles["version"] = 1
        
        try:
            cursor = conn.execute('SELECT ZCODEMESSAGE as code, lower(ZCODETYPE) as code_type, ZSLUG as name FROM ZCDCARDENTITY')
            
            for row in cursor:
                card = dict()
                card["name"] = row["name"]
                card["color"] = "#000000"
                card["code"] = row["code"]
                
                card["code_type"] = row["code_type"].split('.')[-1].replace('-', '')
                if card["code_type"] == "qrcode":
                    card["code_type"] = "qr"
                card["created_at"] = round(time.time() * 1000)  # millisecond timestamp

                handles["cards"].append(card)
        finally:
            conn.close()

        with open(os.path.join(self.output_dir, "sailcards.json"), 'w') as outfile:
            json.dump(handles, outfile, indent=4)


