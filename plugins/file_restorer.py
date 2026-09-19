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
import logging
import shutil
import sqlite3
from ../extractor import Extractor

logger = logging.getLogger(__name__)

class FileRestorer(Extractor):
    
    def get_db_source(self):
        return "Manifest.db"
    
    def apply(self, pattern):
        conn = sqlite3.connect(get_db_source())

        try:
            cursor = conn.execute(
                """
                SELECT fileId, relativePath FROM Files WHERE relativePath LIKE ?
                """,
                (pattern,)
            )

            for file_id, relative_path in cursor:
                # Files are stored as:
                #   <first two characters of fileId>/<fileId>
                source_path = os.path.join(source_root, file_id[:2], file_id)

                # relativePath always uses "/" as its separator.
                destination_path = os.path.join(
                    destination_root,
                    *relative_path.split("/")
                )

                # Create any intermediate directories.
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                logger.info(f"Copying {source_path} to {destination_path}...")
                shutil.copy2(source_path, destination_path)

        finally:
            conn.close()
        
class PictureExtractor(FileRestorer):
    """ Dedicated restorer for images """
    
    def apply(self):
        apply("Media/DCIM%")

class MMSAttachmentExtractor(FileRestorer):
    """ Dedicated restorer for MMS attachments """
    
    def apply(self):
        apply("Library/SMS/Attachments%")
