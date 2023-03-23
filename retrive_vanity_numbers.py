import boto3

def lambda_handler(event, context):
    # Set up DynamoDB resource and table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('phone_no_collection')
    
    # Query the table for the top 3 vanity numbers
    response = table.query(
        IndexName='your_index_name',
        KeyConditionExpression='partition_key = :pk',
        ExpressionAttributeValues={
            ':pk': 'caller_number'
        },
        ScanIndexForward=False,
        Limit=3
    )
    
    # Extract the vanity numbers from the query response
    vanity_numbers = [item['vanity_number'] for item in response['Items']]
    
    # Build the response object for Amazon Connect
    connect_response = {
        'statusCode': 200,
        'status': 'SUCCESS',
        'vanity_numbers': vanity_numbers
    }
    
    return connect_response
