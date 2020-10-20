#!/bin/bash

# Check if the script has been executed from the reservations/ directory
# Move the current directory to it if not in order to execute the script

FILE=../manage.py
if test -f "$FILE"; then
    cd ..
fi


# Dajngo archive

python3 manage.py archive
status=$?

if [ $status -ne 0 ] ;then
    printf ">>> ERROR : command archive has failed\n"
    printf ">>> STATUT : $status\n"
    exit $status
else
    printf ">>> SUCCES : command archive has successed\n"
fi
