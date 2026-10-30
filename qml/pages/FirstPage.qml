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
import Sailfish.Pickers 1.0

Page {
    id: page

    // The effective value will be restricted by ApplicationWindow.allowedOrientations
    allowedOrientations: Orientation.All

    property string directoryPath: ""
    
    Connections {
        target: python
        onEncryptedBackup: pageStack.push(Qt.resolvedUrl("PasswordDialog.qml"))
        onNotABackup: {}
        onDecryptionError: {}
    }

    // To enable PullDownMenu, place our content in a SilicaFlickable
    SilicaFlickable {
        anchors.fill: parent

        // PullDownMenu and PushUpMenu must be declared in SilicaFlickable, SilicaListView or SilicaGridView
        PullDownMenu {
            MenuItem {
                text: qsTr("Select backup folder")
                onClicked: pageStack.push(backupFolderPickerPage)
            }
            MenuItem {
                text: qsTr("About")
                onClicked: pageStack.push(Qt.resolvedUrl("AboutPage.qml"))
            }
        }

        // Tell SilicaFlickable the height of its content.
        contentHeight: column.height

        // Place our content in a Column.  The PageHeader is always placed at the top
        // of the page, followed by our content.
        Column {
            id: column

            width: page.width
            height: page.height
            spacing: Theme.paddingLarge
            PageHeader {
                title: qsTr("iOS to Sailfish")
            }
            Label {
                x: Theme.horizontalPageMargin
                verticalAlignment: "AlignVCenter"
                horizontalAlignment: "AlignHCenter"
                text: qsTr("Please select the folder containing backup data")
                visible: directoryPath === ""
            }
        }
    }
    
    Component {
        id: backupFolderPickerPage
        FolderPickerPage {
            dialogTitle: qsTr("Select backup folder")
            showSystemFiles: true
            onSelectedPathChanged: {
                page.directoryPath = selectedPath
                pageStack.pop()
                python.forwardDirectory(page.directoryPath)
            }
        }
    }

}
