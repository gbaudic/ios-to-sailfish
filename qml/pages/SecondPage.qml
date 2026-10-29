/* 
 * ios-to-sailfish - A collection of Python scripts to easily migrate from iOS to SailfishOS
 * Copyright (c) 2026 G. Baudic
 *
 * ios-to-sailfish is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * ios-to-sailfish is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.0
import Sailfish.Silica 1.0
import Sailfish.Contacts 1.0
import io.thp.pyotherside 1.4

Page {
    id: selectPage
    
    property bool isMigrating: false
    property bool isEncrypted: false
    
    property int contactCount: 0
    property int callCount: 0
    property int podcastCount: 0
    property int documentCount: 0
    property int noteCount: 0
    property int eventCount: 0
    property int mediaCount: 0
    property int loyaltyCount: 0
    property int messageCount: 0

    // The effective value will be restricted by ApplicationWindow.allowedOrientations
    allowedOrientations: Orientation.All

    SilicaListView {
        id: listView
        model: [
            { name: qsTr("Contacts (%1)").arg(contactCount), 
              count: contactCount,
              enabled: contactCount > 0,
              description: qsTr("Migrate the contacts with ContactImporter") },
            { name: qsTr("Call history (%1)").arg(callCount), 
              count: callCount,
              enabled: isEncrypted && callCount > 0,
              description: qsTr("Migrate the call history") },
            { name: qsTr("Podcast subscriptions (%1)").arg(podcastCount), 
              count: podcastCount,
              enabled: podcastCount > 0,
              description: qsTr("Export the podcast subscriptions to an OPML file, suitable for import in AntennaPod or gPodder. Podcast downloads are not managed.") },
            { name: qsTr("Documents (%1)").arg(documentCount), 
              count: documentCount,
              enabled: documentCount > 0,
              description: qsTr("Migrate application documents to your Documents folder") },
            { name: qsTr("Notes (%1)").arg(noteCount), 
              count: noteCount,
              enabled: noteCount > 0,
              description: qsTr("Export the notes to your Documents folder") },
            { name: qsTr("Calendar events (%1)").arg(eventCount), 
              count: eventCount,
              enabled: eventCount > 0,
              description: qsTr("Export all events as an .ics file") },
            { name: qsTr("Photos and Videos (%1)").arg(mediaCount), 
              count: mediaCount,
              enabled: mediaCount > 0,
              description: qsTr("Migrate the photos and videos to their respective folders") },
            { name: qsTr("Loyalty cards (%1)").arg(loyaltyCount), 
              count: loyaltyCount,
              enabled: loyaltyCount > 0,
              description: qsTr("Export data from Fira as a JSON file compatible with Sailcards. Wallet is not supported yet") },
            { name: qsTr("Messages (%1)").arg(messageCount), 
              count: messageCount,
              enabled: messageCount > 0,
              description: qsTr("Migrate SMS, MMS and RCS messages with their attachments") }
        ]
        anchors.fill: parent
        header: PageHeader {
            title: qsTr("Select data to migrate")
        }
        delegate: ListItem {
            id: delegate
            contentHeight: Theme.itemSizeMedium
            property var itemData: model
            property alias checked: checkbox.checked

            TextSwitch {
                id: checkbox
                text: itemData.name
                description: itemData.description
                checked: itemData.enabled
                enabled: itemData.enabled
            }
            ProgressBar {
                width: parent.width
                minimumValue: 0
                maximumValue: itemData.count
                value: 0
                valueText: value === maximumValue ? qsTr("Done") : qsTr("%1 / %2").arg(value).arg(maximumValue)
                visible: isMigrating && checkbox.checked
            }
            
            onClicked: console.log("Clicked " + index)
        }
        VerticalScrollDecorator {}
        
        PullDownMenu {
            MenuItem {
                text: qsTr("Start migration")
                onClicked: { 
                    remorse.execute(qsTr("Migrating..."), doMigrate)
                }
            }
        }
        
        RemorsePopup { id: remorse }
    }
    
    Component {
        id: errorDialogComponent
        Dialog {
            property string messageText: ""
            Column {
                width: parent.width
                spacing: Theme.paddingLarge
                DialogHeader { title: qsTr("Error") }
                Label {
                    x: Theme.horizontalPageMargin
                    width: parent.width - 2 * Theme.horizontalPageMargin
                    wrapMode: Text.Wrap
                    color: Theme.errorColor
                    text: messageText
                }
            }
        }
    }
    
    ContactImporter {
        id: contactImporter
    }

    function showError(msg) {
        pageStack.push(errorDialogComponent, { messageText: msg })
    }
    
    function doMigrate() {
        isMigrating = true
    }
    
    function importContact(vcard) {
        contactImporter.importContactsData(vcard)
    }
}
