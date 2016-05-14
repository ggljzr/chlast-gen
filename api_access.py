import json
import requests
import base64

#kolem to query musi bejt '%27tenstring%27'
#ty %27 se pridavaj v ty tride booze pri volani
#konstruktoru jak se generuje ten link ale mozna by se to mohlo delat tady
def get_image_url(query, api_key):

    credential_string = ':' + api_key
    credential_string = credential_string.encode('UTF-8')
    credential_string = base64.b64encode(credential_string)

    credential_string = 'Basic {}'.format(credential_string.decode('UTF-8'))
    top = 20
    offset = 0
    url = 'https://api.datamarket.azure.com/Bing/Search/Image?' + \
        'Query=%s&$top=%d&$skip=%d&$format=json' % (query, top, offset)

    request = requests.get(url, headers = {'Authorization' : credential_string})

    results = request.json()

    return results['d']['results'][0]['MediaUrl']
