import json
import os
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
def analyze(latest):
    insights=[]
    s = latest.get('bloodPressureSystolic')
    d = latest.get('bloodPressureDiastolic')
    sugar = latest.get('bloodSugar')
    sleep = latest.get('sleepHours')
    steps = latest.get('steps')
    if s and d:
        try:
            s = float(s); d = float(d)
            if s>140 or d>90:
                insights.append('Consider consulting a physician for high blood pressure.')
            elif s<90 or d<60:
                insights.append('Low blood pressure detected; ensure hydration.')
        except:
            pass
    if sugar:
        try:
            sugar=float(sugar)
            if sugar>180:
                insights.append('High blood sugar detected; review diet and medication.')
            elif sugar<70:
                insights.append('Low blood sugar detected; have a quick carbohydrate snack.')
        except:
            pass
    if sleep:
        try:
            sleep=float(sleep)
            if sleep<6:
                insights.append('Increase sleep duration; aim for 7-8 hours.')
        except:
            pass
    if steps:
        try:
            steps=int(steps)
            if steps<3000:
                insights.append('Try increasing daily steps to at least 5000.')
        except:
            pass
    if not insights:
        insights.append('All metrics look within typical ranges. Keep it up!')
    return insights
def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    user_id = params.get('userId')
    if not user_id:
        return {'statusCode':400,'body':json.dumps({'error':'userId required'})}
    resp = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('userId').eq(user_id),ScanIndexForward=False,Limit=1)
    items = resp.get('Items',[])
    if not items:
        return {'statusCode':404,'body':json.dumps({'error':'no records found'})}
    latest = items[0]
    insights = analyze(latest)
    return {'statusCode':200,'body':json.dumps({'insights':insights,'latest':latest})}
