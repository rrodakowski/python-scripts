
DEPLOYDIR=/app-bin

echo "Deploying $TAR to $DEPLOYDIR"
cd $DEPLOYDIR
rm -rf services
cp $DIR/$TAR $DEPLOYDIR
tar -xvf $TAR
rm $TAR

sudo service apache2 restart

