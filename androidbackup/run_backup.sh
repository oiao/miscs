#!/usr/bin/env bash

if [ ! -f "target_files.txt" ]
then
    echo "target_files.txt does not exist, exiting."
	exit 1
fi

mkdir tmpbak

# Read `target_files.txt`, adb pull every line
while read LINE
do
	if [[ $LINE != \#* ]] && [[ ! -z $LINE ]]
	then
		echo Pulling $LINE
		adb pull $LINE tmpbak/.
	fi
done < target_files.txt

duplicity tmpbak file://backup

rm tmpbak -r
echo All Done!
