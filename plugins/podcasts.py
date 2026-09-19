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

import io
import logging
import os
import os.path
import xml.dom.minidom
import sqlite3
import sys
from ../extractor import Extractor
from email.utils import formatdate

logger = logging.getLogger(__name__)


class PodcastExtractor(Extractor):
    """Export a list of channel objects to a local file in OPML 1.1 format.

    See www.opml.org for the OPML specification.
    """
    
    def __init__(self):
        self.filename = "Podcasts.opml"
    
    def get_db_source(self):
        return "398be25b8d2881e4a18865f018eb5d8e3c8fc962"
        
# Code from gPodder opml.py
    def apply(self):
        """Write an XML document containing metadata for each podcast in the database.

        OPML 2.0 specification: http://www.opml.org/spec2
        """

        doc = xml.dom.minidom.Document()

        opml = doc.createElement('opml')
        opml.setAttribute('version', '2.0')
        doc.appendChild(opml)

        head = doc.createElement('head')
        head.appendChild(self.create_node(doc, 'title', 'Podcasts subscriptions'))
        head.appendChild(self.create_node(doc, 'dateCreated', formatdate(localtime=True)))
        opml.appendChild(head)

        body = doc.createElement('body')
        
        conn = sqlite3.connect(get_db_source())
        conn.row_factory = sqlite3.Row

        try:
            cursor = conn.execute("""SELECT
                    ZTITLE, ZITEMDESCRIPTION, ZFEEDURL, ZWEBPAGEURL
                FROM ZMTPODCAST WHERE ZSUBSCRIBED = 1
            """)

            for row in cursor:
                body.appendChild(self.createOutline(doc,
                    row["ZTITLE"],
                    row["ZITEMDESCRIPTION"],
                    row["ZFEEDURL"],
                    row["ZWEBPAGEURL"],
                )

        finally:
            conn.close()
        
        opml.appendChild(body)

        try:
            data = doc.toprettyxml(encoding='utf-8', indent='    ', newl=os.linesep)
            with open(self.filename, 'wb') as fp:
                fp.write(data)

        except:
            logger.error('Could not open file for writing: %s', self.filename,
                    exc_info=True)

    def create_node(self, doc, name, content):
        """Return an XML Element node with tag name "name" and text content "content".

        E.g. <name>content</name>.
        """
        node = doc.createElement(name)
        node.appendChild(doc.createTextNode(content))
        return node

    def create_outline(self, doc, title, text, xml_url, html_url):
        """Return an OPML outline as XML Element node in the supplied document."""
        outline = doc.createElement('outline')
        outline.setAttribute('title', title)
        outline.setAttribute('text', text)
        outline.setAttribute('xmlUrl', xml_url)
        if html_url is not None:
            outline.setAttribute('htmlUrl', html_url)
        outline.setAttribute('type', 'rss')
        return outline

