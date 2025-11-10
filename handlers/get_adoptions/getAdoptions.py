import boto3
import os
import json

# Write a Lambda function that returns a 200 status and "connected" message ensure it Create a DynamoDB resource, Connect to a table with the environment variable named ADOPTIONS_TABLE, Scan the table to get all items from the table and put it in a variable, Prepare the response with the appropriate HTTP status code of 200, headers, and body. Headers should allow requests from any origin. The headers should have GET, HEAD, and OPTIONS methods for access control allow methods.
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['APPLICATIONS_TABLE_NAME'])
    items = table.scan()['Items']
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
        },
        'body': json.dumps(items)
    }
    return response
    