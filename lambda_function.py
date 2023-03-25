import boto3
import requests

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vanity_numbers')

def lambda_handler(event, context):
    phone_number = event['phone_number'] #('17500046841')
    caller_number = event['caller_number'] #('1800344337')
    vanity_numbers = get_vanity_numbers(phone_number)
    best_vanity_numbers = get_best_vanity_numbers(vanity_numbers)
    save_to_dynamodb(best_vanity_numbers, caller_number,phone_number)
    return {
        'statusCode': 200,
        'body': 'Saved best vanity numbers to DynamoDB'
    }


def get_vanity_numbers(phone_number):
    """
    Returns a list of possible vanity numbers for the given phone number
    """
    letters = {
        '1': {'I'},
        '2': {'A', 'B', 'C'},
        '3': {'D', 'E', 'F'},
        '4': {'G', 'H', 'I'},
        '5': {'J', 'J', 'L'},
        '6': {'M', 'N', 'O'},
        '7': {'P', 'Q', 'R', 'S'},
        '8': {'T', 'U', 'V'},
        '9': {'W', 'X', 'Y', 'Z'},
        '0': {'O'}
    }

    def generate_vanity_numbers(digits, current=''):
        if not digits:
            return [current]
        else:
            digit = digits[0]
            rest = digits[1:]
            combinations = []
            for letter in letters[digit]:
                combinations += generate_vanity_numbers(rest, current + letter)
            return combinations

    digits = [digit for digit in phone_number if digit.isdigit()]
    return generate_vanity_numbers(digits)


def get_best_vanity_numbers(vanity_numbers):
    """
    Returns the best 5 vanity numbers based on some criteria
    """
    # Define a list of English words using the Datamuse API
    response = requests.get('https://api.datamuse.com/words?sl={combination}', params={'max': 5})
    english_words = set([word['word'] for word in response.json()])
    
    # Return with top 5 vanity numbers
    return [english_words]

def save_to_dynamodb(vanity_numbers, caller_number, phone_number):
    """
    Saves the best 5 vanity numbers and the caller's number to DynamoDB
    """
    items = []
    items_to_put = []
    for vanity_number in vanity_numbers:
        item = {
            'phone_number': phone_number,
            'vanity_number': vanity_number,
            'caller_number': caller_number
        }
        #items.append(item)
    
    # Sort the items based on some criteria before saving
    items = sorted(items, key=lambda x: x['vanity_number'])
    
    # Save only the top 5 items
    items_to_put = items[:5]
    
    if item['vanity_number'] not in [item['vanity_number'] for item in items_to_put]:
                items_to_put.append(item)
    else:
                # If the item key already exists, generate a new ID and add the item again
                item['vanity_number'] #= str(uuid.uuid4())
                items_to_put.append(item)
    
    # Batch write the items to DynamoDB
    with table.batch_writer() as batch:
        for item in items_to_put:
            batch.put_item(Item=item)