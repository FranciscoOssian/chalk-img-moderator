from flask import Flask, request, jsonify, abort
import os
from utils import try_add_to_proxy, validate_request, validate_image_request
from nsfw_detector import predict
from ImageCollector import ImageCollector

app = Flask(__name__)

img_dim = 299
model = predict.load_model(f"./model/nsfw.{img_dim}x{img_dim}.h5")

try_add_to_proxy()

@app.route('/predict_url', methods=['POST'])
def predict_image_url():

  error = validate_request(request)
  if error:
    return jsonify(error[0]), error[1]
  
  url = request.json.get('url')
  
  image = ImageCollector(url)

  img_path, error = image.create()

  if error:
    return jsonify({'error': error[0]}), error[1]

  prediction = predict.classify(
    model=model,
    input_paths=img_path,
    image_dim=img_dim
  )

  image.dispose()

  return jsonify(prediction[img_path])


@app.route('/predict_image', methods=['POST'])
def predict_image_file():
    
    error = validate_image_request(request)
    if error:
      return jsonify(error[0]), error[1]
    
    file = request.files['file']

    image = ImageCollector(file)

    img_path, error = image.create()
    if error:
        return jsonify({'error': error[0]}), error[1]

    prediction = predict.classify(
        model=model,
        input_paths=img_path,
        image_dim=img_dim
    )

    image.dispose()

    return jsonify(prediction[img_path])