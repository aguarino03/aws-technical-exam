#import boto3
import json

def lambda_handler(event, context):
    
    # Get the phone number from the event
    phone_number = ('618001657478')
    
    # Initialize the DynamoDB client
    dynamodb = boto3.client('dynamodb')
    
    # Get the top 3 vanity numbers for the phone number from the DynamoDB table
    response = dynamodb.query(
        TableName='phone_no_collection',
        KeyConditionExpression='caller_number = :caller_number',
        ExpressionAttributeValues={
            ':caller_number': {'S': phone_number}
        },
        ProjectionExpression='vanity_number',
        Limit=3,
        ScanIndexForward=False
    )
    
    # Extract the vanity numbers from the DynamoDB response
    vanity_numbers = []
    for item in response['Items']:
        vanity_numbers.append(item['vanity_number'])
    
    # Send the vanity numbers back to Amazon Connect
    return {
        "statusCode": 200,
        "body": json.dumps({
            "vanity_numbers": vanity_numbers
        })
    }
