from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 從環境變數讀取 Access Token 和 Channel Secret
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/")
def home():
    return "LINE Bot is running."

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    print(f"🔍 [DEBUG] Signature: {signature}")
    print(f"🔍 [DEBUG] Body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ Invalid signature.")
        abort(400)

    return 'OK'

# 處理收到的訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    reply = f"你說了：{msg}"
    print(f"📨 [REPLY] {reply}")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
