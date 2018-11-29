# 處理使用者輸入的訊息
# 要等很久
import json
from bottle import route, run, request
#from send_msg import send_text_message

PORT = 200

@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('REQUEST BODY: ')
    print(json.dumps(body, indent=2))
    

run(host="localhost", port=PORT, debug=True)
