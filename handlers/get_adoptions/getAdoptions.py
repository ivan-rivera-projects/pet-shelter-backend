import boto3
import os
import json

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['APPLICATIONS_TABLE_NAME'])
        items = table.scan()['Items']
        
        response_body = {
            'message': 'Successfully got adoptions',
            'adoptions': items,
            'count': len(items)
        }
        
        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
            },
            'body': json.dumps(response_body)
        }
        return response
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
    