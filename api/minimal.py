import json

def handler(event, context):
    """最简单的 Vercel Python 函数"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "status": "ok",
            "message": "Minimal test works"
        })
    }
