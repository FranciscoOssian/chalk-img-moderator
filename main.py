from flask import Flask, request, jsonify
import os
from utils import try_add_to_proxy, validate_request

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from nsfw_detector import predict

from ImageCollector import ImageCollector

app = Flask(__name__)

img_dim = 299
model = predict.load_model(f"./model/nsfw.{img_dim}x{img_dim}.h5")

try_add_to_proxy()

@app.route('/predict', methods=['GET'])
def predict_image():

  error = validate_request(request)
  if error:
    return jsonify(error[0]), error[1]

  image = ImageCollector(request.json['url'])

  img_path, error = image.create()
  if error:
    return jsonify({'error':error[0]}), error[1]

  prediction = predict.classify(
    model = model,
    input_paths = img_path,
    image_dim = img_dim
  )

  image.dispose()

  return jsonify(prediction[img_path])