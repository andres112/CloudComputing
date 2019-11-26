from flask import Flask, request
import boto3

dynamo_client = boto3.client('dynamodb')

TABLE_NAME = 'watches'

def get_watch(sku):
    try:
        response = dynamo_client.get_item(
            TableName = 'watches',
            Key={
                'sku': {'S': sku}
            }
        )
    except Exception as e:
        print(str(e))
    else:
        return response.get('Item')

def put_watch():
    sku = request.json.get('sku')
    if not sku:
        return {'error': 'Please provide a sku'}
    
    if get_watch(sku):
        return {'error': 'Register for sku {} is already created'.format(sku)}        

    try:
        kind = request.json.get('type') if request.json.get('type') else "WATCH"
        year = request.json.get('year') if request.json.get('year') else "2019"
        status = request.json.get('status') if request.json.get('status') else "OLD"
        movement = request.json.get('movement') if request.json.get('movement') else "NO DATA"
        gender = request.json.get('gender') if request.json.get('gender') else "MAN"
        dial_material = request.json.get('dial_material') if request.json.get('dial_material') else "NO DATA"
        dial_color = request.json.get('dial_color') if request.json.get('dial_color') else "NO DATA"
        case_material = request.json.get('case_material') if request.json.get('case_material') else "NO DATA"
        case_form = request.json.get('case_form') if request.json.get('case_form') else "NO DATA"
        bracelet_material = request.json.get('bracelet_material') if request.json.get('bracelet_material') else "NO DATA"  
    
        response = dynamo_client.put_item(
            TableName = TABLE_NAME,
            Item={
                'sku': {'S': sku },
                'type': {'S': kind },
                'year': {'N': year },
                'status': {'S': status },
                'movement': {'S': movement },
                'gender': {'S': gender },
                'dial_material': {'S': dial_material },
                'dial_color': {'S': dial_color },
                'case_material': {'S': case_material },
                'case_form': {'S': case_form },
                'bracelet_material': {'S': bracelet_material }
            }
        )
    except Exception as e:
        print(str(e))
        return {"error": '{} was not created'.format(sku)}
    else:
        return {"sku": '{} created successfully'.format(sku)}
