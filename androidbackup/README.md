Android Backup with Duplicity
=============================
* Creates a tar ball on the device from `target_files.txt`
* `adb pull`s the archive to local machine
* Optionally encrypts it with GPG

Requirements
------------
* Android Debug Bridge: `apt install adb`

Usage
-----
* Connect device (check with `adb devices`)
* Edit the `target_files.txt`
* Run `./run_backup.sh`
* To restore an archive, use `gpg -d ARCHIVE.tgz.gpg | tar xz`
* Encryption can be disabled when the `--nogpg` flag is passed
