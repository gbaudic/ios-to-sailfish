# ios-to-sailfish
A collection of Python scripts to ease migration from iOS to SailfishOS

## Supported data

  * MMS attachments, as-is
  * Pictures and videos, as-is
  * SMS/MMS/RCS messages (text only), as a JSON file for import with commhistory
  * Podcasts, as an OPML file compatible with gPodder and AntennaPod
  * Recordings, as-is
  * User files, as-is
  * Loyalty cards from Fira, as a JSON file for Sailcards
  
## NOT supported data

  * Notes: export them as text or Markdown and get them as User files
  * Call history: only available in encrypted backups
  * WLAN credentials
  * Reminders, unless they have a date set in which case they will appear in the Calendar data

## Usage

As a command-line tool (will export everything):

    python3 ios2sailfish.py <backup directory> <output directory>

Or as a very basic GUI (allows you to choose what to export):

    python3 ios2sailfish_ui.py

## Requirements

  * Python 3.x, currently developed with 3.14 but should support earlier versions as well
  * An unencrypted backup of your phone, made for example with iTunes

## License

GPL v3, see LICENSE file for the full text

## Extra credits

  * gpodder (GPLv3): inspiration for the OPML export logic
  * https://github.com/soyersoyer/ios-sms-export-to-sailfish for the SMS export code
