import boto3
import os
import json

# Connect to the DynamoDB table
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ['ADOPTIONS_TABLE'])

def lambda_handler(event, context):

    try:

        # Get the adoption ID from the event
        id = event.get('pathParameters', {}).get('id', '')

        # Retrieve the adoption item by its ID

        response = table.get_item(
            Key={
                'id': id
            }
        )

        # Check if the item exists
        if 'Item' in response:
            item = response['Item']
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token, X-Amz-User-Agent"
                },

                "body": json.dumps(item)

            }

        # If the item does not exist, return a 404
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token, X-Amz-User-Agent"
                },
                "body": json.dumps({"message": "Adoption details not found for id " + str(id)})
            }

    # Return a 500 if an exception is thrown
    except Exception as e:

        # Return a server error if the get_item operation fails
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving adoption details: ' + str(e))
        }