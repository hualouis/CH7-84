from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('mlMIoXx0OEtv8B+AqOQhZPL4cww2YvqiBCBxx6S7nZIa0pNfWIpc1yAUTyBvtHYmYmGbuAN3XDr9ls0GgQZBd//mqKNVq3jxhkbcOVGs90d39rNQ6e4tKG7aURK2+dXRtiCq/5fXYl3s28rr4zFf5AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5429cb61345aaa978fb617ca130a99dc')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()