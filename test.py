import os
from io import BytesIO

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, MessageEvent, TextMessage,
                            TextSendMessage)

import settings
from vision import get_text_by_ms

app = Flask(__name__)


line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)

endpoint = 'https://eastasia.api.cognitive.microsoft.com/vision/v1.0'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("body:", body)

    # handle webhook body
    try:
        handler.handle(body, signature)

    except InvalidSignatureError as e:
        print("InvalidSignatureError:", e)
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("handle_message:", event)
    text = event.message.text

    if (text.startswith('http')):
        image_text = get_text_by_ms(text)
        reply_message(event, TextSendMessage(text=image_text))
        return

    messages = [
        TextSendMessage(text=text),
        TextSendMessage(text='画像のURLを送ってみてね!'),
    ]

    reply_message(event, messages)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    print("handle_image:", event)

    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    image = BytesIO(message_content.content)

    image_text = get_text_by_ms(image=image)
    reply_message(event, TextSendMessage(text=image_text))


def reply_message(event, messages):
    line_bot_api.reply_message(
        event.reply_token,
        messages=messages,
    )


if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )
