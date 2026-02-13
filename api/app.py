from flask import Flask, jsonify, request
from jmcomic import *
import requests
import logging
import sys
from io import BytesIO
from PIL import Image
from urllib.parse import unquote, re

sys.stdout.reconfigure(encoding="utf-8")

app = Flask(__name__)
app.debug = False
app.json.ensure_ascii = False

# 存储捕获的图片
captured_images = {}

# 保存原始的save_image方法
original_save_image = JmImageTool.save_image

@classmethod
def new_save_image(cls, image: Image.Image, filepath: str):
    captured_images[filepath] = image

JmImageTool.save_image = new_save_image

@classmethod
def new_try_mkdir(cls, save_dir: str):
    return save_dir

JmcomicText.try_mkdir = new_try_mkdir

def decode_search_value(value: str) -> str:
    url_encoded_pattern = r"%[0-9A-Fa-f]{2}"
    if re.search(url_encoded_pattern, value):
        try:
            decoded = unquote(value)
            while re.search(url_encoded_pattern, decoded):
                temp = unquote(decoded)
                if temp == decoded:
                    break
                decoded = temp
            return decoded
        except Exception:
            return value
    else:
        return value

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "JMComic API is running"})

@app.route("/config", methods=["GET"])
def config():
    api_url = request.host_url.rstrip("/")
    return jsonify({
        "JMComic": {
            "name": "JMComic",
            "apiUrl": api_url,
            "detailPath": "/album/<id>",
            "photoPath": "/photo/<id>/chapter/<chapter>",
            "searchPath": "/search/<text>/<page>",
            "type": "jmcomic"
        }
    })

# Vercel serverless handler
def handler(request):
    with app.request_context(request.environ):
        try:
            response = app.full_dispatch_request()
            return response.get_data(), response.status_code, response.headers.items()
        except Exception as e:
            return str(e), 500

# 为了本地测试保留
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
