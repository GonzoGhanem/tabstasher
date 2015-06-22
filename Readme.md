# Sublime Tabstasher 0.2-alpha

Tabstasher will allow you to stash the current opened tabs under a common name. You can later untash either by apply or pop methods, like the git stash does, and reopen the tab sessions.

# Installation

### Package Control
Using [Package Control](http://wbond.net/sublime_packages/package_control), a
package manager for Sublime Text.

Press "cmd + shift + p" and then type "Package Control: Add Repository", press enter.

Use 'https://github.com/GonzoGhanem/tabstasher.git'

Press "cmd + shift + p" again and then type "Package Control: Install Package", press enter.

Once the list of packages is displayed, simply search for 'tabstasher' and press enter.

## How it works

Access all available commands by opening command palette (cmd + shift + p) and typing Tabstasher. Available options and brief explanation below.

- **Stash opened files:** This will prompt user to enter an identifier to be used as the stash name and will close all opened files in the current window after saving.

- **Stash apply from list:** User will be presented with a list of stashes currently saved, upon selection stashed tabs will be re opened and the stash will remain as it is.

- **Stash pop from list:** User will be presented with a list of stashes currently saved, upon selection stashed tabs will be re opened and the stash will be removed from the list of stashes.

- **Stash pop last:** This command will pick the last (most recent) saved stash from which stashed tabs will be re opened and the stash will be removed from the list of stashes.

- **Delete a stash:** User will be presented with a list of stashes currently saved, upon selection the selected stash will be removed from the list of stashes.

- **Clear all stashes:** Command will remove all saved stashes in the list of stashes.

> NOTE: Any apply/pop command, will Close current tabs opened before opening the stashed tabs.

## Added git support on v0.2
Press cmd + shift + p and search for "Tabstasher: is this a git repo??" option. If set as Yes, tabstasher will also create a git stash using the same stash name provided by the user when stashing opened tabs. Same will happen when doing stash pop/apply commands and delete or clear.

## License
* MIT License

2015 - Created by Gonzo Ghanem