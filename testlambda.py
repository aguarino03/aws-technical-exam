import json
import urllib.parse
import urllib.request

def lambda_handler(event, context):
    # Get the phone number from the event
    phone_number = ('18004685865')

    # Format the phone number into a query string for the Datamuse API
    query = "http://api.datamuse.com/words?md=p&max=1&sp="
    query += "".join(['2ABC'[int(digit)] for digit in str(phone_number)])

    # Send a GET request to the Datamuse API and parse the response
    response = urllib.request.urlopen(query)
    data = json.loads(response.read().decode())

    # Extract the vanity word from the response and return it
    vanity_word = data[0]['word']
    return {
        'vanity_number': vanity_word
    }
