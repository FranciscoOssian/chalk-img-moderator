import requests
import os
import hashlib

def imageConvert(url):
  # Baixar a imagem
  response = requests.get(url)
  img_data = response.content

  # Criar o diretório se não existir
  if not os.path.exists('./content/images/convert/'):
    os.makedirs('./content/images/convert/')

  # Gerar o nome do arquivo a partir do hash da URL
  filename = hashlib.sha256(url.encode()).hexdigest() + '.jpg'

  # Salvar a imagem
  img_path = './content/images/convert/' + filename
  with open(img_path, 'wb') as img_file:
    img_file.write(img_data)

  return img_path