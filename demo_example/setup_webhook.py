# 伺服器執行
# 先run ngrok (指令是 ngrok.exe http <port>)
# 注意PORT可能In Bind
from bottle import route, run, request

PORT = 200
VERIFY_TOKEN = "Messenger_Chatbot"


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

run(host="localhost", port=PORT, debug=True)
