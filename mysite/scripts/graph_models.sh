#!/bin/bash

# Check if the script has been executed from the twahifoundation/ directory
# Move the current directory to it if not in order to execute the script

FILE=../manage.py
if test -f "$FILE"; then
    cd ..
fi


# Modelization of the entire project

python3 manage.py graph_models -a -g -o graph_models/entire_project_visualization.png
status=$?

if [ $status -ne 0 ] ;then
    printf ">>> ERROR : command graph_models COMPLETE PROJECT has failed\n"
    printf ">>> STATUT : $status\n"
    exit $status
else
    printf ">>> SUCCES : command graph_models COMPLETE PROJECT success\n"
fi

# Modelization  entire project without edge

python3 manage.py graph_models -a --hide-edge-labels -g -o graph_models/no_edge_entire_project_visualization.png
status=$?

if [ $status -ne 0 ] ;then
    printf ">>> ERROR : command graph_models COMPLETE NO EDGE PROJECT has failed\n"
    printf ">>> STATUT : $status\n"
    exit $status
else
    printf ">>> SUCCES : command graph_models COMPLETE NO EDGE PROJECT success\n"
fi

# Modelization including certaine model

python manage.py graph_models -a -I User,Group,Permission,Company,Person,Event,Project,Stock,Product,ProductStockTransfert,Category,Task,Transaction,ProductTransactionLine,Message,Newsletter,Post,Tags,AbstractNotification,Notification,ContentType -o graph_models/sub_tf_visualization.png
status=$?

if [ $status -ne 0 ] ;then
    printf ">>> ERROR : command graph_models SUB PROJECT has failed\n"
    printf ">>> STATUT : $status\n"
    exit $status
else
    printf ">>> SUCCES : command graph_models SUB PROJECT success\n"
fi

# Modelization  without edge

python manage.py graph_models -a --hide-edge-labels -I User,Group,Permission,Company,Person,Event,Project,Stock,Product,ProductStockTransfert,Category,Task,Transaction,ProductTransactionLine,Message,Newsletter,Post,Tags,AbstractNotification,Notification,ContentType  -o graph_models/no_edge_sub_tf_visualization.png
status=$?

if [ $status -ne 0 ] ;then
    printf ">>> ERROR : command graph_models SUB NO EDGE PROJECT has failed\n"
    printf ">>> STATUT : $status\n"
    exit $status
else
    printf ">>> SUCCES : command graph_models SUB NO EDGE PROJECT success\n"
fi