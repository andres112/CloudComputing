import boto3
import json

dynamodb = boto3.resource('dynamodb', 'eu-north-1')

def batch_write(table_name, items):
    table = dynamodb.Table(table_name)

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
    return True

def read_json(json_file, list):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    for item in data['watches']:
        list.append(item) 

if __name__ == '__main__':
    table_name = 'watches'
    json_file = 'db/watches.json'
    watches = []

    read_json(json_file, watches)
    status = batch_write(table_name, watches)

    if status:
        print('Data loaded successfully')
    else:
        print('It has ocurred an error loading the data...')