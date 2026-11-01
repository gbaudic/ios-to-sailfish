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

Page {
    id: selectPage
    
    property bool isMigrating: false
    property bool isEncrypted: false
    property bool isComplete: false

    // The effective value will be restricted by ApplicationWindow.allowedOrientations
    allowedOrientations: Orientation.All
    
    Connections {
        target: python
        function onMigrationComplete() {
            isMigrating = false
            isComplete = true
        }
        function onPythonError(message) {
            Notices.show(message)
        }
        function onMigrationProgress(key, count) {
            for (var i = 0; i < model.count ; i++) {
                if (model.get(i).key === key) {
                    model.setProperty(i, "currentCount", count)
                    break
                }
            }
        }
        function onAnalysisComplete(key, count) {
            for (var i = 0; i < model.count ; i++) {
                if (model.get(i).key === key) {
                    model.setProperty(i, "count", count)
                    break
                }
            }
        }

    }
    
    ListModel {
        id: model
        ListElement {
            name: QT_TR_NOOP("Contacts (%1)")
            key: "contacts"
            count: 0
            currentCount: 0
            checked: true
            enabled: count > 0 && !isMigrating
            description: QT_TR_NOOP("Migrate the contacts with ContactImporter")
        }
        ListElement {
            name: QT_TR_NOOP("Call history (%1)")
            key: "calls"
            count: 0
            currentCount: 0
            checked: true
            enabled: isEncrypted && count > 0 && !isMigrating
            description: QT_TR_NOOP("Migrate the call history")
        }
        ListElement {
            name: QT_TR_NOOP("Podcast subscriptions (%1)")
            key: "podcasts"
            count: 0
            currentCount: 0
            checked: true
            enabled: count > 0 && !isMigrating
            description: QT_TR_NOOP("Export the podcast subscriptions to an OPML file, suitable for import in AntennaPod or gPodder. Podcast downloads are not managed.")
        }
        ListElement {
            name: QT_TR_NOOP("Documents (%1)")
            key: "documents"
            count: 0
            currentCount: 0
            checked: true
            enabled: count > 0 && !isMigrating
            description: QT_TR_NOOP("Migrate application documents to your Documents folder")
        }
        ListElement {
            name: QT_TR_NOOP("Notes (%1)")
            key: "notes"
            count: 0
            currentCount: 0
            checked: true
            enabled: count > 0 && !isMigrating
            description: QT_TR_NOOP("Export the notes to your Documents folder")
        }
        ListElement {
            name: QT_TR_NOOP("Calendar events (%1)")
            key: "events"
            count: 0
            currentCount: 0
            checked: true
            enabled: count > 0 && !isMigrating
            description: QT_TR_NOOP("Export all events as an .ics file")
        }
        ListElement {
            name: QT_TR_NOOP("Photos and Videos (%1)")
            key: "media"
            count: 0
            currentCount: 0
            checked: true
            enabled: count > 0 && !isMigrating
            description: QT_TR_NOOP("Migrate the photos and videos to their respective folders")
        }
        ListElement {
            name: QT_TR_NOOP("Loyalty cards (%1)")
            key: "loyalty"
            count: 0
            currentCount: 0
            checked: true
            enabled: count > 0 && !isMigrating
            description: QT_TR_NOOP("Export data from Fira as a JSON file compatible with Sailcards. Wallet is not supported yet")
        }
        ListElement {
            name: QT_TR_NOOP("Messages (%1)")
            key: "messages"
            count: 0
            currentCount: 0
            checked: true
            enabled: count > 0 && !isMigrating
            description: QT_TR_NOOP("Migrate SMS, MMS and RCS messages with their attachments")
        }
    }

    Label {
        id: migrationResult
        anchors.fill: parent
        visible: isComplete
        font.pixelSize: Theme.fontSizeLarge
        wrapMode: Text.Wrap
        verticalAlignment: "AlignVCenter"
        horizontalAlignment: "AlignHCenter"
        text: qsTr("Migration completed! You can now close this app")
    }

    SilicaListView {
        id: listView
        model: model
        visible: !isComplete
        anchors.fill: parent
        header: PageHeader {
            title: qsTr("Select data to migrate")
        }
        delegate: ListItem {
            id: delegate
            contentHeight: Theme.itemSizeMedium
            property var itemData: model
            property string name: model.key

            TextSwitch {
                id: checkbox
                width: listView.width
                text: qsTr(itemData.name).arg(itemData.count)
                description: qsTr(itemData.description)
                checked: itemData.checked
                enabled:  {
                    var result = itemData.count > 0 && !isMigrating
                    if (itemData.key === "calls") {
                        result = result && isEncrypted
                    }
                    return result
                }
            }
            ProgressBar {
                id: progressBar
                anchors.top: checkbox.bottom
                width: listView.width
                minimumValue: 0
                maximumValue: itemData.count
                value: itemData.currentCount
                valueText: value === maximumValue ? qsTr("Done") : qsTr("%1 / %2").arg(value).arg(maximumValue)
                visible: (isMigrating || isComplete) && checkbox.checked
            }
            
            onClicked: console.log("Clicked " + index)
        }
        VerticalScrollDecorator {}
        
        PullDownMenu {
            MenuItem {
                text: qsTr("Start migration")
                onClicked: { 
                    if (!isComplete && !isMigrating) {  // Avoid repeated runs
                        remorse.execute(qsTr("Migrating..."), doMigrate)
                    } else {
                        Notices.show(qsTr("Migration already done"), Notice.Short)
                    }
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
                DialogHeader {
                    title: qsTr("Error")
                }
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
        // Identify what to migrate
        var migrations = []
        for (var i = 0; i < model.count ; i++) {
            var element = model.get(i)
            if (element.checked) {
                migrations.push(element.key)
            }
        }

        // Basic sanity check
        if (migrations.length === 0) {
            Notices.show(qsTr("No migration selected"))
        } else {
            isMigrating = true
            python.migrate(migrations)
        }
    }
    
    function importContact(vcard) {
        contactImporter.importContactsData(vcard)
    }
}
