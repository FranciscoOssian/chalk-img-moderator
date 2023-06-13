import re
import requests
import os
import hashlib
import random
import string

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
    
    if 'key' not in request.json:
        return {'error': f'The "key" field is required in the request body'}, 400
    
    server_key = os.environ.get('PYTHON_SERVER_KEY')
    
    if server_key is None or request.json['key'] != server_key:
        return {'error': f'The "key" field is wrong in the request body'}, 400
    
    if not isinstance(request.json['url'], str):
        return {'error': 'The "url" field must be a string'}, 400

    return None