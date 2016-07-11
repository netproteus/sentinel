from decimal import Decimal
import boto3



def get_metadata(config):
    session = boto3.session.Session(aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'], region_name=config['aws_region'])
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(config['table'])
    item = table.get_item(Key={'name': '_metadata'})

    if 'Item' not in item:
        return {}

    item = item['Item']
    item.pop('name')
    for k, v in item.items():
        if isinstance(v, Decimal):
            item[k] - float(v)
    return item


def set_metadata(config, data):
    session = boto3.session.Session(aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'], region_name=config['aws_region'])
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(config['table'])
    data['name'] = '_metadata'
    table.put_item(Item=data)


def get_alert_data(config, name):
    session = boto3.session.Session(aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'], region_name=config['aws_region'])
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(config['table'])
    item = table.get_item(Key={'name': name})

    if 'Item' not in item:
        return {
            'keys': {}
        }

    item = item['Item']
    item.pop('name')
    for k, v in item.items():
        if isinstance(v, Decimal):
            item[k] - float(v)
    return item


def set_alert_data(config, name, data):
    session = boto3.session.Session(aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'], region_name=config['aws_region'])
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(config['table'])
    data['name'] = name
    table.put_item(Item=data)
