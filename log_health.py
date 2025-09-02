import json
import os
import uuid
import time
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
def validate_record(body):
    allowed_keys = {'userId','bloodPressureSystolic','bloodPressureDiastolic','bloodSugar','sleepHours','steps','notes','timestamp'}
    return any(k in body for k in allowed_keys)
def lambda_handler(event, context):
    body = json.loads(event.get('body') or '{}')
    if not validate_record(body):
        return {'statusCode':400,'body':json.dumps({'error':'invalid payload'})}
    record_id = str(uuid.uuid4())
    timestamp = body.get('timestamp') or int(time.time())
    item = {
        'userId': body['userId'],
        'recordId': 'log#' + record_id,
        'timestamp': int(timestamp),
    }
    for k,v in body.items():
        if k!='userId':
            item[k]=v
    table.put_item(Item=item)
    return {'statusCode':201,'body':json.dumps({'recordId':record_id})}
