#!/usr/bin/env bash

# --nogpg flag to disable encryption
X=true
for arg in $@
do
  if [ $arg = --nogpg ]
  then
    X=false
  fi
done

TARGETS="target_files.txt"
if [ ! -f $TARGETS ]
then
    echo "$TARGETS does not exist, exiting."
	exit 1
fi

FNAME=bak$(date +"%y%m%d_%k%M").tar.gz

echo "Pushing targets"
adb push $TARGETS /sdcard/$TARGETS
echo "Creating archive"
adb shell tar -T /sdcard/$TARGETS -czvf /sdcard/$FNAME
echo "Pulling archive"
adb pull /sdcard/$FNAME .
echo "Cleaning device"
adb shell rm /sdcard/$FNAME /sdcard/$TARGETS

# Encrypt
if $X
then
  gpg -c $FNAME # Will ask for a passpharase
  # gpg -c --batch --passphrase MYSECRETKEY $FNAME # Will use the provided passphrase
  rm $FNAME
fi

echo All Done!
