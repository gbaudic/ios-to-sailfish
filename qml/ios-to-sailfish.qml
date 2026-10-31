import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.4
import "pages"

ApplicationWindow {
    initialPage: Component { FirstPage { } }
    cover: Qt.resolvedUrl("cover/CoverPage.qml")
    allowedOrientations: defaultAllowedOrientations

    Python {
        id: python

        property string backup_version: '1.0'
        property string ui_version: '0.1'
        property string backupDirectory

        signal encryptedBackup()
        signal notABackup()
        signal decryptionError()
        signal analysisComplete(string type, int count)
        signal migrationReady()
        signal migrationProgress(string type, int index)
        signal migrationComplete()
        signal pythonError(string message)

        Component.onCompleted: {
            setHandler('encrypted-backup', encryptedBackup)
            setHandler('not-a-backup', notABackup)
            setHandler('decryption-error', decryptionError)
            setHandler('migration-ready', migrationReady)

            addImportPath(Qt.resolvedUrl('.'));

            importModule('bridge', function () {});
        }

        function migrate(types) {
            call('bridge.migrate', [types])
        }

        function forwardPassword(password) {
            // Reattempt to open backup using user-supplied password
            call('bridge.open_backup', [backupDirectory, password])
        }

        function forwardDirectory(directory) {
            backupDirectory = directory
            call('bridge.open_backup', [directory])
        }

        onError: {
            console.error('Python failure: ', traceback);
        }
    }
}
