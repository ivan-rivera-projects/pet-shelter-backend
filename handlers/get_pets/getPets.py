import json
import os
import boto3
from botocore.exceptions import ClientError

# Environment variables
table_name = os.environ.get('PETS_TABLE_NAME', 'Pets')
region = os.environ.get('AWS_REGION', 'us-east-1')

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    """
    Lambda function handler to retrieve all pets from DynamoDB.

    This function is invoked by API Gateway when a GET request is made to /pets.
    It scans the Pets DynamoDB table and returns all pet records.

    Args:
        event: API Gateway event object containing request details
        context: Lambda context object with runtime information

    Returns:
        dict: API Gateway response with statusCode, headers, and body
    """

    # CORS headers for cross-origin requests
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,OPTIONS'
    }

    try:
        # Scan the DynamoDB table to get all pets
        response = table.scan()
        pets = response.get('Items', [])

        # Handle pagination if there are more items
        # DynamoDB Scan operations return max 1MB of data per call
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            pets.extend(response.get('Items', []))

        # Return successful response with pets data
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Successfully got pets',
                'pets': pets
            })
        }

    except ClientError as e:
        # Handle DynamoDB-specific errors
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        print(f"DynamoDB ClientError: {error_code} - {error_message}")

        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'message': 'Internal server error',
                'error': f"{error_code}: {error_message}"
            })
        }

    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {str(e)}")

        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'message': 'Internal server error',
                'error': str(e)
            })
        }
