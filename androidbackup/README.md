Android Backup and Encrypt
==========================
* Creates a tarball on the Android device from `target_files.txt`
* `adb pull`s the archive to local machine
* Optionally encrypts it with GPG

Requirements
------------
* [Android Debug Bridge](https://developer.android.com/studio/command-line/adb)

Usage
-----
* Connect device (check with `adb devices`)
* Edit the `target_files.txt`
* Run `./run_backup.sh`
* To restore an archive, use `gpg -d ARCHIVE | tar xz`
* Encryption can be disabled when the `--nogpg` flag is passed
