from flask import Flask, request, jsonify
from flask_cors import CORS
import replicate
from PIL import Image
import io
import base64
import requests

app = Flask(__name__)
CORS(app)

# Add your Replicate API Token
replicate.Client(api_token="YOUR_REPLICATE_API_KEY")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    data = request.json
    image_data = data.get("image")
    image_bytes = base64.b64decode(image_data.split(",")[1])

    # Background removal model
    output = replicate.run(
        "cjwbw/rembg:1.0.1",
        input={"image": image_bytes}
    )
    return jsonify({"result": output})

@app.route("/upscale", methods=["POST"])
def upscale():
    data = request.json
    image_data = data.get("image")
    image_bytes = base64.b64decode(image_data.split(",")[1])

    # 4K upscale model
    output = replicate.run(
        "nightmareai/real-esrgan:latest",
        input={
            "image": image_bytes,
            "scale": 4
        }
    )
    return jsonify({"result": output})

@app.route("/resize-passport", methods=["POST"])
def resize_passport():
    data = request.json
    image_data = data.get("image")
    image_bytes = base64.b64decode(image_data.split(",")[1])
    image = Image.open(io.BytesIO(image_bytes))

    # Passport photo standard size = 2x2 inches at 300 DPI
    target_size = (600, 600)
    image = image.resize(target_size)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({"result": f"data:image/jpeg;base64,{encoded}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)