Android Backup with Duplicity
=============================
`adb pull`s all files in `target_files.txt` with to the local machine
and creates a backup with duplicity afterwards.

Requirements
------------
* Android Debug Bridge: `apt install adb`
* Duplicity `apt install duplicity`

Usage
-----
* Edit the `target_files.txt`
* Run `./run_backup.sh`



