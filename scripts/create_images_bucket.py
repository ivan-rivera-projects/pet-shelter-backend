#!/usr/bin/env python3
"""
Script to create an S3 bucket for storing pet images.
This script follows the class curriculum structure.

The bucket is configured with:
- Public read access for images
- CORS configuration for cross-origin requests from the frontend
- Unique bucket name using AWS account ID and timestamp

Usage:
    python scripts/create_images_bucket.py
"""

import boto3
import json
from datetime import datetime

# Initialize boto3 clients
s3_client = boto3.client('s3')
sts_client = boto3.client('sts')


def create_images_bucket():
    """
    Create an S3 bucket for storing pet images with proper CORS configuration.

    Returns:
        str: The name of the created bucket
    """
    # Get AWS account ID for unique bucket naming
    account_id = sts_client.get_caller_identity()['Account']

    # Get current region
    region = s3_client.meta.region_name

    # Create unique bucket name
    timestamp = datetime.now().strftime('%Y%m%d')
    bucket_name = f'images-{account_id}-{timestamp}'

    print(f"Creating S3 bucket: {bucket_name}")
    print(f"Region: {region}")

    try:
        # Create the bucket
        if region == 'us-east-1':
            # us-east-1 doesn't require LocationConstraint
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            # Other regions require LocationConstraint
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        print(f"✓ Bucket {bucket_name} created successfully in {region}.")

        # Remove block public access settings
        s3_client.delete_public_access_block(Bucket=bucket_name)
        print(f"✓ Block public access turned off for {bucket_name}.")

        # Set bucket policy to allow public read access to images
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/images/*"
                }
            ]
        }

        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        print(f"✓ Public read policy applied to {bucket_name}/images/")

        # Configure CORS for cross-origin access from the website
        cors_configuration = {
            'CORSRules': [
                {
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET', 'HEAD'],
                    'AllowedOrigins': ['*'],
                    'ExposeHeaders': ['ETag'],
                    'MaxAgeSeconds': 3000
                }
            ]
        }

        s3_client.put_bucket_cors(
            Bucket=bucket_name,
            CORSConfiguration=cors_configuration
        )
        print(f"✓ CORS configuration applied to {bucket_name}")

        print(f"\n{'='*60}")
        print(f"SUCCESSFULLY COMPLETED. Bucket name is: {bucket_name}")
        print(f"{'='*60}")
        print(f"\nNext steps:")
        print(f"1. Upload images: cd pet-shelter-client/src/assets")
        print(f"2. Run: aws s3 cp . s3://{bucket_name}/images/ --recursive")
        print(f"3. Set frontend .env variable:")
        print(f"   VITE_PET_IMAGES_BUCKET_URL='https://{bucket_name}.s3.{region}.amazonaws.com/images'")

        return bucket_name

    except Exception as e:
        print(f"✗ Error creating bucket: {str(e)}")
        raise


if __name__ == '__main__':
    # Run the bucket creation function when script is executed
    create_images_bucket()
