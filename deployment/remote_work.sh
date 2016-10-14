# properties 
# don't have the deply.properties on remote server so use
# properties here, passed into this script are:
# $TAR and $DIR
DEPLOYDIR=/app-bin

echo "Deploying $TAR to $DEPLOYDIR"
cd $DEPLOYDIR
rm -rf services
cp $DIR/$TAR $DEPLOYDIR
tar -xvf $TAR
rm $TAR

sudo service apache2 restart

echo "deploy successfully finished"

