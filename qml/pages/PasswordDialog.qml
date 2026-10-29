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

Dialog {
    id: passwordDialog
    
    property string password

    Column {
        width: parent.width

        DialogHeader { 
            title: qsTr("Encrypted backup detected")
            defaultAcceptText: qsTr("Decrypt")
        }
        
        Label {
            wrapMode: Text.WordWrap
            text: qsTr("Your backup is encrypted. Enter the password below to decrypt it and continue.")
            color: Theme.highlightColor
            width: parent.width
        }

        PasswordField {
            id: passwordField
            width: parent.width
            showEchoModeToggle: true
            
            EnterKey.enabled: text.length > 0
            EnterKey.iconSource: "image://theme/icon-m-enter-accept"
            EnterKey.onClicked: passwordDialog.accept()
        }
        
        Label {
            id: errorLabel
            text: ""
            color: Theme.errorColor
            font.pixelSize: Theme.fontSizeSmall
            visible: false
        }
    }

    onDone: {
        if (result == DialogResult.Accepted) {
            password = passwordField.text
            if (password.length === 0) {
                errorLabel.visible = true
                errorLabel.text = qsTr("Password cannot be empty")
            }
        }
    }
}
