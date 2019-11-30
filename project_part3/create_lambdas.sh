echo "******** Creating new directory"
mkdir watches
cd watches/

# sudo apt install awscli
# aws configure

echo "******* Virtual environment creation and activation"
virtualenv env
source env/bin/activate

echo "********* Copying web service files in directory"
cp ../server.py .
cp ../app_controller.py .

echo "********* Installing required dependencies"
pip install flask flask-cors boto3 simplejson

echo "********* Installing zappa"
pip install zappa

sleep 10 & wait
zappa init & wait $!

sleep 10 & wait
echo "******* Deploying zappa"
zappa deploy dev