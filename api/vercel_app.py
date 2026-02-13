from flask import Flask, jsonify
import sys
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "API is running"})

@app.route('/config')
def config():
    return jsonify({
        "JMComic": {
            "name": "JMComic",
            "apiUrl": "https://manhua.vercel.app",
            "detailPath": "/album/<id>",
            "photoPath": "/photo/<id>/chapter/<chapter>",
            "searchPath": "/search/<text>/<page>",
            "type": "jmcomic"
        }
    })

# Vercel handler
def handler(event, context):
    with app.test_request_context(
        path=event.get("path", "/"),
        method=event.get("httpMethod", "GET"),
        headers=event.get("headers", {}),
        query_string=event.get("queryStringParameters", {})
    ):
        try:
            response = app.full_dispatch_request()
            return {
                "statusCode": response.status_code,
                "headers": dict(response.headers),
                "body": response.get_data(as_text=True)
            }
        except Exception as e:
            print(traceback.format_exc())
            return {
                "statusCode": 500,
                "body": jsonify({"error": str(e)}).get_data(as_text=True)
            }
