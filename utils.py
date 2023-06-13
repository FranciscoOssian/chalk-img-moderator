import re
import requests

def try_add_to_proxy():
    try:
        # Definir a URL e a chave secreta do servidor Node.js
        node_server_url = 'http://localhost:3000/update-servers'
        secret_key = 'xxx123'

        # Informar o servidor Node.js sobre a presença deste servidor Python
        response = requests.post(node_server_url, json={'host': 'localhost', 'port': 8000, 'key': secret_key})

        print("# Informar o servidor Node.js sobre a presença deste servidor Python")
        print(node_server_url, 'feito', response)
    except:
        print('error: add to proxy')
        pass

def validate_request(request):
    if not request.is_json:
        return {'error': 'Request body must be a JSON object'}, 400
    if 'url' not in request.json or not isinstance(request.json['url'], str):
        return {'error': 'The "url" field is required in the request body and it must be a string'}, 400
    return None