from decimal import Decimal
import boto3



def decimals_to_floats(obj):
    if isinstance(obj, list):
        for i in xrange(len(obj)):
            obj[i] = decimals_to_floats(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.iterkeys():
            obj[k] = decimals_to_floats(obj[k])
        return obj
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj


def floats_to_decimals(obj):
    if isinstance(obj, list):
        for i in xrange(len(obj)):
            obj[i] = floats_to_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.iterkeys():
            obj[k] = floats_to_decimals(obj[k])
        return obj
    elif isinstance(obj, float):
        return Decimal(obj)
    else:
        return obj


def get_metadata(config):
    session = boto3.session.Session(aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'], region_name=config['aws_region'])
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(config['table'])
    item = table.get_item(Key={'name': '_metadata'})

    if 'Item' not in item:
        return {}

    item = item['Item']
    item.pop('name')
    return decimals_to_floats(item)


def set_metadata(config, data):
    session = boto3.session.Session(aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'], region_name=config['aws_region'])
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(config['table'])
    data['name'] = '_metadata'
    table.put_item(Item=floats_to_decimals(data))


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
    return decimals_to_floats(item)


def set_alert_data(config, name, data):
    session = boto3.session.Session(aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'], region_name=config['aws_region'])
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(config['table'])
    data['name'] = name
    table.put_item(Item=floats_to_decimals(data))
