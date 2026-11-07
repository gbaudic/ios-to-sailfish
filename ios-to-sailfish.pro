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
TARGET = harbour-appleseed

CONFIG += sailfishapp_qml

SOURCES +=

DEPLOY_PATH = /usr/share/$${TARGET}

backup.files = ios-backup-core/src/*
backup.path = $${DEPLOY_PATH}/

INSTALLS += \
    backup

DISTFILES += qml/harbour-appleseed.qml \
    qml/bridge.py \
    qml/cover/CoverPage.qml \
    qml/pages/AboutPage.qml \
    qml/pages/FirstPage.qml \
    qml/pages/PasswordDialog.qml \
    qml/pages/SelectionPage.qml \
    rpm/harbour-appleseed.changes.in \
    rpm/harbour-appleseed.changes.run.in \
    rpm/harbour-appleseed.spec \
    translations/*.ts \
    harbour-appleseed.desktop

SAILFISHAPP_ICONS = 86x86 108x108 128x128 172x172

# to disable building translations every time, comment out the
# following CONFIG line
CONFIG += sailfishapp_i18n

TRANSLATIONS += translations/harbour-appleseed-fr.ts
