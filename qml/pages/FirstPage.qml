import QtQuick 2.0
import Sailfish.Silica 1.0
import Sailfish.Pickers 1.0
import io.thp.pyotherside 1.4

Page {
    id: page

    // The effective value will be restricted by ApplicationWindow.allowedOrientations
    allowedOrientations: Orientation.All

    property string directoryPath: ""

    // To enable PullDownMenu, place our content in a SilicaFlickable
    SilicaFlickable {
        anchors.fill: parent

        // PullDownMenu and PushUpMenu must be declared in SilicaFlickable, SilicaListView or SilicaGridView
        PullDownMenu {
            MenuItem {
                text: qsTr("Select backup folder")
                onClicked: pageStack.push(backupFolderPickerPage)
            }
        }

        // Tell SilicaFlickable the height of its content.
        contentHeight: column.height

        // Place our content in a Column.  The PageHeader is always placed at the top
        // of the page, followed by our content.
        Column {
            id: column

            width: page.width
            spacing: Theme.paddingLarge
            PageHeader {
                title: qsTr("iOS to Sailfish")
            }
            Label {
                x: Theme.horizontalPageMargin
                verticalAlignment: AlignVCenter
                text: qsTr("Please select the folder containing backup data")
                visible: directoryPath === ""
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
                }
            }
        }
    }

    Python {
        id: python

        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'));

            //importModule('datadownloader', function () {});

        }
    }
}
