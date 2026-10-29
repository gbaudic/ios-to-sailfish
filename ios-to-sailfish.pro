# NOTICE:
#
# Application name defined in TARGET has a corresponding QML filename.
# If name defined in TARGET is changed, the following needs to be done
# to match new name:
#   - corresponding QML filename must be changed
#   - desktop icon filename must be changed
#   - desktop filename must be changed
#   - icon definition filename in desktop file must be changed
#   - translation filenames have to be changed

# The name of your application
TARGET = ios-to-sailfish

CONFIG += sailfishapp_qml

SOURCES +=

DEPLOY_PATH = /usr/share/$${TARGET}

backup.files = ios-backup-core/src/*
backup.path = $${DEPLOY_PATH}/

INSTALLS += \
    backup

DISTFILES += qml/ios-to-sailfish.qml \
    qml/cover/CoverPage.qml \
    qml/pages/AboutPage.qml \
    qml/pages/FirstPage.qml \
    qml/pages/PasswordDialog.qml \
    qml/pages/SecondPage.qml \
    rpm/ios-to-sailfish.changes.in \
    rpm/ios-to-sailfish.changes.run.in \
    rpm/ios-to-sailfish.spec \
    translations/*.ts \
    ios-to-sailfish.desktop

SAILFISHAPP_ICONS = 86x86 108x108 128x128 172x172

# to disable building translations every time, comment out the
# following CONFIG line
CONFIG += sailfishapp_i18n

TRANSLATIONS += translations/ios-to-sailfish-fr.ts
