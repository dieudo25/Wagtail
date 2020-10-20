#!/bin/bash

# Check if the script has been executed from the twahifoundation/ directory
# Move the current directory to it if not in order to execute the script

FILE=../manage.py
if test -f "$FILE"; then
    cd ..
fi


# dump all the data from the account app and django.contrib.auth module in the twahifoundation/account/fixtures directory with the manage.py utility

python3 manage.py dumpdata auth.group --indent 4 > account/fixtures/group.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(0_group.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/account/fixtures'"
    exit $status
else
    printf "(0_group.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi


python3 manage.py dumpdata auth.permission --indent 4 > account/fixtures/permission.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(1_permission.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/account/fixtures'"
    exit $status
else
    printf "(1_permission.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata account.user --indent 4 > account/fixtures/user.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(2_user.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/account/fixtures'"
    exit $status
else
    printf "(2_user.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi



# dump all the data from the project app in the twahifoundation/project/fixtures directory with the manage.py utility

python3 manage.py dumpdata project.project --indent 4 > project/fixtures/project.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(3_project.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/project/fixtures'"
    exit $status
else
    printf "(3_project.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata project.event --indent 4 > project/fixtures/event.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(4_event.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/project/fixtures'"
    exit $status
else
    printf "(4_event.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata project.task --indent 4 > project/fixtures/task.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(5_task.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/project/fixtures'"
    exit $status
else
    printf "(5_task.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi


# dump all the data from the transaction app in the twahifoundation/transaction/fixtures directory with the manage.py utility

python3 manage.py dumpdata transaction.transaction --indent 4 > transaction/fixtures/transaction.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(6_donnatingtransaction.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/transaction/fixtures'"
    exit $status
else
    printf "(6_donnatingtransaction.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata transaction.producttransactionline --indent 4 > transaction/fixtures/product_transaction_line.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(7_product_transaction_line.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/transaction/fixtures'"
    exit $status
else
    printf "(7_product_transaction_line.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi


# dump all the data from the stock app in the twahifoundation/stock/fixtures directory with the manage.py utility

python3 manage.py dumpdata stock.product --indent 4 > stock/fixtures/product.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(8_product.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/stock/fixtures'"
    exit $status
else
    printf "(8_product.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata stock.category --indent 4 > stock/fixtures/category.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(9_category.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/stock/fixtures'"
    exit $status
else
    printf "(9_category.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata stock.stock --indent 4 > stock/fixtures/stock.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(10_stock.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/stock/fixtures'"
    exit $status
else
    printf "(10_stock.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata stock.productstocktransfert --indent 4 > stock/fixtures/product_stock_transfert.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(11_product_stock_transfert.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/stock/fixtures'"
    exit $status
else
    printf "(11_product_stock_transfert.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi


# dump all the data from the contact app in the twahifoundation/contact/fixtures directory with the manage.py utility

python3 manage.py dumpdata contact.person --indent 4 > contact/fixtures/person.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(12_person.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/contact/fixtures'"
    exit $status
else
    printf "(12_person.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata contact.company --indent 4 > contact/fixtures/company.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(13_company.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/contact/fixtures'"
    exit $status
else
    printf "(13_company.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

# dump all the data from the blog app in the twahifoundation/blog/fixtures directory with the manage.py utility

python3 manage.py dumpdata blog.post --indent 4 > blog/fixtures/post.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(14_post.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/blog/fixtures'"
    exit $status
else
    printf "(14_post.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata blog.category --indent 4 > blog/fixtures/category.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(15_category.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/blog/fixtures'"
    exit $status
else
    printf "(15_category.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

python3 manage.py dumpdata blog.tags --indent 4 > blog/fixtures/tags.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(16_tags.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/blog/fixtures'"
    exit $status
else
    printf "(16_tags.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi

# dump all the data from the blog app in the twahifoundation/message/fixtures directory with the manage.py utility

python3 manage.py dumpdata message.message --indent 4 > message/fixtures/message.json
status=$?

if [ $status -ne 0 ] ;then
    printf "(17_message.json)\n>>> ERROR: JSON-data export has failed  (Fixture import error: $status)\n"
    printf "You may check if the data is valid and put in 'twahifoundation/message/fixtures'"
    exit $status
else
    printf "(17_message.json)\n>>> SUCCESS: Fixture JSON-data successfully exported\n"
fi