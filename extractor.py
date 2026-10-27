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

class Extractor(object):
    """ Base class for data extraction plugins """
    
    def __init__(self, input, output):
        self.backup_dir = input
        self.output_dir = output
        self.is_dry_run = False
        
    def set_backup_dir(self, backup):
        self.backup_dir = backup
        
    def set_output_dir(self, output):
        self.output_dir = output
    
    def get_db_source(self):
        raise NotImplementedError
        
    def should_run(self):
        """ Set if this extractor should run """
        return True

    def set_dry_run(self, dry_run):
        """ Toggle dry run (i.e., simulated run) """
        self.is_dry_run = dry_run
        
    def get_absolute_db_source(self):
        db_hash = self.get_db_source()
        if db_hash == "Manifest.db":
            return os.path.join(self.backup_dir, db_hash)
        return os.path.join(self.backup_dir, db_hash[0:2], db_hash)
    
    def min_os_version(self):
        return 1
        
    def max_os_version(self):
        return 99
        
    def apply(self):
        """ Applies the extractor to the data """
        raise NotImplementedError
