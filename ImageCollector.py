import os
import re
import requests
import hashlib

class ImageCollector:
    def __init__(self, url):
        self.url = url
        self.image_path = None

    def _validate(self):
        # Verificar se o URL é uma string
        if not isinstance(self.url, str):
            return None, ('The "url" field must be a string', 400)

        url_pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        if not re.match(url_pattern, self.url):
            return None, ('The "url" field must be a valid URL', 400)

        try:
            response = requests.get(self.url)
            if response.status_code != 200:
                return None, ('The URL is not accessible or valid', 400)

            content_type = response.headers.get('Content-Type')
            if content_type != 'image/jpeg':
                return None, ('The URL does not point to a valid JPEG image', 400)

        except requests.exceptions.RequestException:
            return None, ('An error occurred while accessing the URL', 400)

        return response, None

    def create(self):
        response, error = self._validate()
        if error:
            return None, error
        
        img_data = response.content

        # Criar o diretório se não existir
        if not os.path.exists('./content/images/convert/'):
            os.makedirs('./content/images/convert/')

        # Gerar o nome do arquivo a partir do hash da URL
        filename = hashlib.sha256(self.url.encode()).hexdigest() + '.jpg'

        # Salvar a imagem
        self.image_path = './content/images/convert/' + filename
        with open(self.image_path, 'wb') as img_file:
            img_file.write(img_data)

        return self.image_path, None

    def dispose(self):
        if self.image_path and os.path.exists(self.image_path):
            os.remove(self.image_path)
            self.image_path = None
        else:
            return {'error': 'No file to delete or file not found'}, 400
