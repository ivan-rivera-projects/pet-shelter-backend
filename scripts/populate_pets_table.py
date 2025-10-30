#!/usr/bin/env python3
"""
Script to populate the Pets DynamoDB table with sample pet data.
This script follows the class curriculum structure.

Usage:
    python scripts/populate_pets_table.py
"""

import boto3
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')


def populate_dynamodb():
    """
    Populate the Pets DynamoDB table with sample pet data.

    This function creates sample pet records matching the frontend's
    hardcoded data structure, ensuring a smooth migration to microservices.
    """
    # Reference to the Pets table
    table = dynamodb.Table('Pets')

    # Sample pet data matching the frontend structure
    # Note: DynamoDB stores numbers as Decimal type
    pets_data = [
        {
            'id': Decimal('1'),
            'name': 'Buddy',
            'age': Decimal('2'),
            'species': 'Dog',
            'breed': 'Golden Retriever',
            'date_entered': '2024-07-01',
            'image': 'pet5.jpeg'
        },
        {
            'id': Decimal('2'),
            'name': 'Mittens',
            'age': Decimal('1'),
            'species': 'Cat',
            'breed': 'Siamese',
            'date_entered': '2024-07-10',
            'image': 'pet-image2.jpeg'
        },
        {
            'id': Decimal('3'),
            'name': 'Max',
            'age': Decimal('3'),
            'species': 'Dog',
            'breed': 'Labrador',
            'date_entered': '2024-06-15',
            'image': 'pet-image3.jpeg'
        },
        {
            'id': Decimal('4'),
            'name': 'Whiskers',
            'age': Decimal('2'),
            'species': 'Cat',
            'breed': 'Persian',
            'date_entered': '2024-07-05',
            'image': 'pet-image4.jpeg'
        },
        {
            'id': Decimal('5'),
            'name': 'Rocky',
            'age': Decimal('4'),
            'species': 'Dog',
            'breed': 'German Shepherd',
            'date_entered': '2024-06-20',
            'image': 'pet5.jpeg'
        },
        {
            'id': Decimal('6'),
            'name': 'Luna',
            'age': Decimal('1'),
            'species': 'Cat',
            'breed': 'Maine Coon',
            'date_entered': '2024-07-12',
            'image': 'pet6.jpeg'
        },
        {
            'id': Decimal('7'),
            'name': 'Charlie',
            'age': Decimal('2'),
            'species': 'Dog',
            'breed': 'Beagle',
            'date_entered': '2024-06-25',
            'image': 'pet7.jpeg'
        },
        {
            'id': Decimal('8'),
            'name': 'Shadow',
            'age': Decimal('3'),
            'species': 'Cat',
            'breed': 'British Shorthair',
            'date_entered': '2024-07-08',
            'image': 'pet8.jpeg'
        },
        {
            'id': Decimal('9'),
            'name': 'Duke',
            'age': Decimal('5'),
            'species': 'Dog',
            'breed': 'Bulldog',
            'date_entered': '2024-06-10',
            'image': 'pet9.jpeg'
        }
    ]

    # Insert each pet into the DynamoDB table
    print("Starting to populate Pets table...")
    for pet in pets_data:
        try:
            table.put_item(Item=pet)
            print(f"✓ Added: {pet['name']} ({pet['species']}) - ID: {pet['id']}")
        except Exception as e:
            print(f"✗ Failed to add {pet['name']}: {str(e)}")

    print("\nPopulation complete!")
    print(f"Total pets added: {len(pets_data)}")


if __name__ == '__main__':
    # Run the population function when script is executed
    populate_dynamodb()
