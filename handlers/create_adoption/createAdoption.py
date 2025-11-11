import json
import boto3
import os
import uuid

def lambda_handler(event, context):
    # Create response dictionary
    response = {
        'statusCode': 201,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': ''
    }
    
    try:
        # Connect to DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['ADOPTIONS_TABLE'])
        
        # Get the body of the event
        body = json.loads(event['body'])
        
        # Generate a unique id and add it to the body
        body['id'] = str(uuid.uuid4())
        
        # Insert the body into the table
        table.put_item(Item=body)
        
        # Set response body with the created data
        response['body'] = json.dumps(body)
        
    except Exception as e:
        response['statusCode'] = 500
        response['body'] = json.dumps({'error': str(e)})
    
    return response