import boto3
import json

#ensure the following Create a DynamoDB resource. Connect to a DynamoDB table named AdoptionsTable. Open the JSON file file_name, one of the function parameters. Populate the table with all the items from the JSON file. Print the string "Complete" when finished.
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('AdoptionsTable')
    with open('adoptions.json') as json_file:
        pets = json.load(json_file)
        for i, pet in enumerate(pets):
            if 'id' not in pet:
                pet['id'] = str(i + 1)
            table.put_item(Item=pet)
    return "Complete"

if __name__ == "__main__":
    result = lambda_handler(None, None)
    print(result)
