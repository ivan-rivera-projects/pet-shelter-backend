import json
import os
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

# Environment variables
table_name = os.environ.get('APPLICATIONS_TABLE_NAME', 'Applications')
region = os.environ.get('AWS_REGION', 'us-east-1')

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    """
    Lambda function handler to create a new adoption application.

    This function is invoked by API Gateway when a POST request is made to /applications.
    It validates the input, generates a unique ID, adds a timestamp, and stores
    the application in the Applications DynamoDB table.

    Args:
        event: API Gateway event object containing request details and body
        context: Lambda context object with runtime information

    Returns:
        dict: API Gateway response with statusCode, headers, and body
    """

    # CORS headers for cross-origin requests
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST,OPTIONS'
    }

    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))

        # Validate required fields
        required_fields = ['pet_id', 'pet_name', 'species', 'applicant_name', 'email', 'phone']
        missing_fields = [field for field in required_fields if field not in body]

        if missing_fields:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'message': 'Bad request - missing required fields',
                    'missing_fields': missing_fields
                })
            }

        # Generate unique application ID and timestamp
        application_id = str(uuid.uuid4())
        submitted_at = datetime.utcnow().isoformat()

        # Construct the application item
        application = {
            'applicationId': application_id,
            'pet_id': body['pet_id'],
            'pet_name': body['pet_name'],
            'species': body['species'],
            'pet_image': body.get('pet_image', ''),
            'applicant_name': body['applicant_name'],
            'email': body['email'],
            'phone': body['phone'],
            'submitted_at': submitted_at,
            'status': 'pending'  # Default status
        }

        # Store in DynamoDB
        table.put_item(Item=application)

        # Return successful response with created application
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'message': 'Application submitted successfully',
                'application': application
            })
        }

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'message': 'Invalid JSON in request body',
                'error': str(e)
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
