# aws-technical-exam

This is only for technical exam.


# Function 1: Converting telephone number to vanity.

    
    # Translating phone number to combination of letters
    letters = [mapping[digit] for digit in number]
    combinations = [''.join(chars) for chars in itertools.product(*letters)]
    return combinations
    
    # This section responsible for collecting the top 5 vanity combination then save to dynamodb.
    
    def lambda_handler(event, context):
    phone_number = event['phone_number']
    vanity_numbers = convert_to_vanity(phone_number)
    best_vanity_numbers = sorted(vanity_numbers, key=len)[:5]
    
    item = {
        'caller_number': phone_number,
        'vanity_number': best_vanity_numbers
    }
    
    table.put_item(Item=item)
    
    # The results were output as JSON then send to amazon connect.
    return {
        'statusCode': 200,
        'body': 'Vanity numbers saved to DynamoDB'
    }




# Function 2: Get the top 3 vanity numbers for the phone number from the DynamoDB table
    
    
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
