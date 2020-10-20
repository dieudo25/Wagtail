#!/bin/bash

# Check if the script has been executed from the twahifoundation/ directory
# Move the current directory to it if not in order to execute the script

FILE=../manage.py
if test -f "$FILE"; then
    cd ..
fi


# Make migrations

python3 manage.py makemigrations
status=$?

if [ $status -ne 0 ] ;then
    printf ">>> ERROR : command makemigrations has failed\n"
    printf ">>> STATUT : $status\n"
    exit $status
else
    printf ">>> SUCCES : command makemigrations has successed\n"
fi

# Migrate

python3 manage.py migrate
status=$?

if [ $status -ne 0 ] ;then
    printf ">>> ERROR : command migrate has failed\n"
    printf ">>> STATUT : $status\n"
    exit $status
else
    printf ">>> SUCCES : command migrate has successed\n"
fi