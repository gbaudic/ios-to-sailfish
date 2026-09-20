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

import importlib.util
import inspect
import logging
import os
import sys
import argparse
from extractor import Extractor
from pathlib import Path

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("app.log")
logger.addHandler(file_handler)

parser = argparse.ArgumentParser(description='Export iPhone backup data to Sailfish OS interoperable formats')
parser.add_argument('backup_path', help='Path to backup folder')
parser.add_argument('output_dir', help='Output directory')


def load_plugins(plugin_dir):
    ''' Dynamically find the plugins '''
    plugins = []
    plugin_path = Path(plugin_dir)
    for file in plugin_path.glob("*.py"):
        # Load the module dynamically from the path
        spec = importlib.util.spec_from_file_location(file.stem, file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Find subclasses of Extractor inside the module
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if issubclass(obj, Extractor) and obj is not Extractor:
                logger.info('Found plugin: %s: %s', obj.__name__, obj.__doc__)
                plugins.append(obj(args.backup_path, args.output_dir))

    return plugins


if __name__ == '__main__':
    args = parser.parse_args()
    if not os.path.exists(args.backup_path):
        logger.error('File does not exist')
        sys.exit(1)
    loaded_plugins = load_plugins('plugins')
    for plugin in loaded_plugins:
        logger.info('Running plugin %s', plugin.__class__.__name__)
        try:
            if plugin.should_run():
                plugin.apply()
        except NotImplementedError:
            logger.warn('No implementation, skipping this plugin')
