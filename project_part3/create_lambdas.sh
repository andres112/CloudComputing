echo "******** Creating new directory"
mkdir infov2
cd infov2/

# sudo apt install awscli
# aws configure

echo "******* Virtual environment creation and activation"
python3 -m venv .env
source .env/bin/activate

echo "********* Copying web service files in directory"
cp ../server.py .
cp ../app_controller.py .

echo "********* Installing required dependencies"
pip install flask flask-cors boto3 simplejson

echo "Installing zappa"
pip install zappa

zappa init & wait $!

sleep 5 & wait
echo "Installing zappa"
zappa deploy dev