echo "******** Moving to directory"
cd watches/

# sudo apt install awscli
# aws configure

echo "******* Virtual environment activation"
source env/bin/activate & wait $!

sleep 10 & wait
echo "******* Updating zappa"
zappa update dev