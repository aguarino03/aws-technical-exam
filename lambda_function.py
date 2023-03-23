import boto3
import itertools 

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('phone_no_collection')

def convert_to_vanity(number):
    mapping = {
		'0': ['0'],
		'1': ['1'],
        '2': ['A', 'B', 'C'],
        '3': ['D', 'E', 'F'],
        '4': ['G', 'H', 'I'],
        '5': ['J', 'K', 'L'],
        '6': ['M', 'N', 'O'],
        '7': ['P', 'Q', 'R', 'S'],
        '8': ['T', 'U', 'V'],
        '9': ['W', 'X', 'Y', 'Z']
    }
    
    letters = [mapping[digit] for digit in number]
    combinations = [''.join(chars) for chars in itertools.product(*letters)]
    return combinations

def lambda_handler(event, context):
    caller_number = ('618001657478')
    vanity_numbers = convert_to_vanity(caller_number)
    best_vanity_numbers = sorted(vanity_numbers, key=len)[:5]
    
    item = {
        'caller_number': caller_number,
        'vanity_number': best_vanity_numbers
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': 'Vanity numbers saved to DynamoDB'
    }