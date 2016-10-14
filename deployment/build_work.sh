file="./deploy.properties"

if [ -f "$file" ]
then
    echo "$file found."
    . $file

    DEST_USER_PW=$1

    #Build Server Work
    echo "Jenkins HOME: $JENKINS_HOME"
    echo "Worskpace: "${WORKSPACE}
    echo "Home: $HOME"
    echo "Date: $DATE"
 
    tar -cvf $HOME/$TAR_FILE -C $WORKSPACE services 
    #tar -cvf $HOME/$TAR_FILE -C $WORKSPACE/services . # this will grab everything in dir 
    scp $HOME/$TAR_FILE $DEST_USER@$DEST_HOST:$DEST_DIR

    echo "Removing the tar file"
    rm $HOME/$TAR_FILE

    # Password will have to be set as environment variable
    ssh $DEST_USER@$DEST_HOST 'echo '"${DEST_USER_PW}"' | sudo -Sv && DIR="'$DEST_DIR'" TAR="'$TAR_FILE'" bash -s' < remote_work.sh
else
    echo "$file not found."
fi

