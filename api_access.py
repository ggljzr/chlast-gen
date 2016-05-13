import json
import requests

def get_image_url(query):

    credentialBing = 'Basic OlU5T0kxYWVLNzZTS2NocUZhS0JnMWMwSUNsaTVlRWV0bllqVXpTcEo2R2c='
    top = 20
    offset = 0

    url = 'https://api.datamarket.azure.com/Bing/Search/Image?' + \
        'Query=%s&$top=%d&$skip=%d&$format=json' % (query, top, offset)

    request = requests.get(url, headers = {'Authorization' : credentialBing})

    results = request.json()

    return results['d']['results'][0]['MediaUrl']
