import itertools
import requests
import json
import os
import boto3

def lambda_handler(event, context):
    # Retrieve phone number from event input
    phone_number = event['phone_number']
    caller_number = event['caller_number']
    
    # Define the mapping of digits to letters
    digit_to_letters = {
        '2': 'ABC',
        '3': 'DEF',
        '4': 'GHI',
        '5': 'JKL',
        '6': 'MNO',
        '7': 'PQRS',
        '8': 'TUV',
        '9': 'WXYZ'
    }
    
    # Generate all possible combinations of letters for the phone number
    letters = [digit_to_letters[digit] for digit in phone_number]
    combinations = list(itertools.product(*letters))
    
    # Convert each combination to a string and filter out any non-alphanumeric characters
    results = []
    for combination in combinations:
        vanity_number = ''.join(combination)
        if vanity_number.isalnum():
            results.append(vanity_number)
    
    # Score each result by sending a GET request to the Datamuse API
    scores = {}
    for result in results:
        url = 'https://api.datamuse.com/words?rel_trg=' + result + '&max=1'
        response = requests.get(url)
        if response.status_code == 200:
            score = json.loads(response.text)[0]['score']
            scores[result] = score
    
    # Sort the results by score and select the top 5
    sorted_results = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    top_5 = sorted_results[:5]
    
    # Save the top 5 results and caller's number to a DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['Best']
    table = dynamodb.Table(table_name)
    
    item = {
        'caller_number': caller_number,
        'phone_number': phone_number,
        'vanity_numbers': top_5
    }
    
    table.put_item(Item=item)
    
    # Return the top 5 results
    return {'top_5': top_5}
