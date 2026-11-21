# ios-to-sailfish
A collection of Python scripts to ease migration from iOS to SailfishOS

Currently slowly turning into an actual SailfishOS app, building on [ios-backup-core](https://github.com/charleswest775/ios-backup-core) for better iOS backup handling.

## Script collection

### Supported data

  * MMS attachments, as-is
  * Pictures and videos, as-is
  * SMS/MMS/RCS messages (text only), as a JSON file for import with commhistory-tool
  * Podcasts, as an OPML file compatible with gPodder and AntennaPod
  * Voice memos, as-is
  * User files, as-is
  * Loyalty cards from Fira, as a JSON file for Sailcards
  * Calendar events, as a single .ics file
  
### NOT supported data

  * Notes: export them as text or Markdown and get them as User files
  * Call history: only available in encrypted backups
  * Contacts
  * WLAN credentials
  * Reminders, unless they have a date set in which case they will appear in the Calendar data

### Usage

As a command-line tool (will export everything):

    python3 ios2sailfish.py <backup directory> <output directory>

Or as a very basic GUI (allows you to choose what to export):

    python3 ios2sailfish_ui.py

## App

In addition to the supported data above, app will rely on ios-backup-core to handle also:

  * Encrypted backups
  * Call history
  * Browser history
  * Notes
  * Contacts

## Requirements

  * Python 3.x, currently developed with 3.14 but should support versions from 3.10 as well
  * An unencrypted backup of your phone, made for example with iTunes

## License

GPL v3, see LICENSE file for the full text

## Extra credits

  * gpodder (GPLv3): inspiration for the OPML export logic
  * https://github.com/soyersoyer/ios-sms-export-to-sailfish for the SMS export code
