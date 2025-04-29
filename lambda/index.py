import json
import os
import urllib.request

# 独自API（Google Colabなど）へのURL
CUSTOM_API_URL = os.environ.get("CUSTOM_API_URL", "https://2d8d-34-139-40-97.ngrok-free.app/")  # 必要に応じて書き換え

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        
        # リクエストボディの取得
        body = json.loads(event['body'])
        message = body['message']
        conversation_history = body.get('conversationHistory', [])
        
        print("Processing message:", message)
        
        # 独自APIに渡すデータを準備
        payload = {
            "message": message,
            "conversationHistory": conversation_history
        }

        # HTTP POSTリクエストを作成
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            CUSTOM_API_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        # APIにリクエスト送信
        with urllib.request.urlopen(req) as res:
            response_body = res.read()
            response_json = json.loads(response_body)

        print("Custom API response:", json.dumps(response_json))

        # 応答と履歴を取得
        assistant_response = response_json.get('response', "（応答なし）")
        updated_history = response_json.get('conversationHistory', [])

        # 正常レスポンスとして返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": updated_history
            })
        }

    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
