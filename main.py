from flask import Flask, request, jsonify
import os
from nsfw_detector import predict

from imageConvert import imageConvert

app = Flask(__name__)

img_dim = 299
model = predict.load_model(f"./model/nsfw.{img_dim}x{img_dim}.h5")

@app.route('/predict', methods=['GET'])
def predict_image():
    url = request.json['url']
    img_path = imageConvert(url)
    prediction = predict.classify(
          model = model,
          input_paths = img_path,
          image_dim = img_dim
      )
    os.remove(img_path)

    return jsonify(prediction[img_path])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
