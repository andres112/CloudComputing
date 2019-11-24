echo "*** Creating Table"
aws dynamodb create-table --cli-input-json file://db/create-table.json & 
wait $!
echo "*** Preparing Things to Load Table"
sleep 5 &
wait
echo "*** Loading Table"
python db/loadDB.py
echo "*** Finish Task"

