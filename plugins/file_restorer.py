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
import extractor

logger = logging.getLogger()

class FileRestorer(extractor.Extractor):
    """ Abstract class for pure file extractors """
    
    def get_db_source(self):
        return "Manifest.db"
    
    def apply(self, pattern):
        conn = sqlite3.connect(self.get_absolute_db_source())

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
                source_path = os.path.join(self.backup_dir, file_id[:2], file_id)

                # relativePath always uses "/" as its separator.
                destination_path = os.path.join(
                    self.output_dir,
                    *relative_path.split("/")
                )

                # Create any intermediate directories.
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                logger.info(f"Copying {source_path} to {destination_path}...")
                try:
                    shutil.copy2(source_path, destination_path)
                except FileNotFoundError:
                    logger.warn('Referenced file does not exist')

        finally:
            conn.close()
            
    def should_run(self):
        return False
        
class PictureExtractor(FileRestorer):
    """ Dedicated restorer for images """
    
    def apply(self):
        super().apply("Media/DCIM%")
        
    def should_run(self):
        return True

class MMSAttachmentExtractor(FileRestorer):
    """ Dedicated restorer for MMS attachments """
    
    def apply(self):
        super().apply("Library/SMS/Attachments%")
    
    def should_run(self):
        return True
