#!/bin/bash

# Check if the script has been executed from the twahifoundation/ directory
# Move the current directory to it if not in order to execute the script

FILE=../manage.py
if test -f "$FILE"; then
    cd ..
fi


# Loads all the JSON-fixtures available in the twahifoundation/account/fixtures directory with the manage.py utility

for file in account/fixtures/*
do
    python3 manage.py loaddata $file
    status=$?

    if [ $status -ne 0 ] ;then
        printf "($file >>> Fixture import error: $status)\n>>> ERROR: JSON-data import has failed\n"
        printf "You may check if the data is valid and put in 'twahifoundation/account/fixtures'"
        exit $status
    else
        printf "($file)\n>>> SUCCESS: Fixture JSON-data successfully imported\n"
    fi
done

# Loads all the JSON-fixtures available in the twahifoundation/contact/fixtures directory with the manage.py utility

for file in contact/fixtures/*
do
    python3 manage.py loaddata $file
    status=$?

    if [ $status -ne 0 ] ;then
        printf "($file >>> Fixture import error: $status)\n>>> ERROR: JSON-data import has failed\n"
        printf "You may check if the data is valid and put in 'twahifoundation/contact/fixtures'"
        exit $status
    else
        printf "($file)\n>>> SUCCESS: Fixture JSON-data successfully imported\n"
    fi
done


# Loads all the JSON-fixtures available in the twahifoundation/project/fixtures directory with the manage.py utility

for file in project/fixtures/*
do
    python3 manage.py loaddata $file
    status=$?

    if [ $status -ne 0 ] ;then
        printf "($file >>> Fixture import error: $status)\n>>> ERROR: JSON-data import has failed\n"
        printf "You may check if the data is valid and put in 'twahifoundation/project/fixtures'"
        exit $status
    else
        printf "($file)\n>>> SUCCESS: Fixture JSON-data successfully imported\n"
    fi
done

# Loads all the JSON-fixtures available in the twahifoundation/stock/fixtures directory with the manage.py utility

for file in stock/fixtures/*
do
    python3 manage.py loaddata $file
    status=$?

    if [ $status -ne 0 ] ;then
        printf "($file >>> Fixture import error: $status)\n>>> ERROR: JSON-data import has failed\n"
        printf "You may check if the data is valid and put in 'twahifoundation/stock/fixtures'"
        exit $status
    else
        printf "($file)\n>>> SUCCESS: Fixture JSON-data successfully imported\n"
    fi
done

printf "\n------------------------------------------------------\n SUCCESS: All fixture JSON-data successfully imported \n------------------------------------------------------\n"
exit 0


# Loads all the JSON-fixtures available in the twahifoundation/transaction/fixtures directory with the manage.py utility

for file in transaction/fixtures/*
do
    python3 manage.py loaddata $file
    status=$?

    if [ $status -ne 0 ] ;then
        printf "($file >>> Fixture import error: $status)\n>>> ERROR: JSON-data import has failed\n"
        printf "You may check if the data is valid and put in 'twahifoundation/transaction/fixtures'"
        exit $status
    else
        printf "($file)\n>>> SUCCESS: Fixture JSON-data successfully imported\n"
    fi
done

printf "\n------------------------------------------------------\n SUCCESS: All fixture JSON-data successfully imported \n------------------------------------------------------\n"
exit 0


# Loads all the JSON-fixtures available in the twahifoundation/blog/fixtures directory with the manage.py utility

for file in blog/fixtures/*
do
    python3 manage.py loaddata $file
    status=$?

    if [ $status -ne 0 ] ;then
        printf "($file >>> Fixture import error: $status)\n>>> ERROR: JSON-data import has failed\n"
        printf "You may check if the data is valid and put in 'twahifoundation/blog/fixtures'"
        exit $status
    else
        printf "($file)\n>>> SUCCESS: Fixture JSON-data successfully imported\n"
    fi
done

