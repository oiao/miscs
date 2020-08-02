Android Backup with Duplicity
=============================
`adb pull`s all files in `target_files.txt` to the local machine
and creates a duplicity backup in the _./backup_ folder.

Requirements
------------
* Android Debug Bridge: `apt install adb`
* Duplicity `apt install duplicity`

Usage
-----
* Edit the `target_files.txt`
* Run `./run_backup.sh`



