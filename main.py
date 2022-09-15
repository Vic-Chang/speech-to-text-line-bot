import aiohttp
import configparser
from fastapi import Request, FastAPI, HTTPException
from linebot import (AsyncLineBotApi, WebhookParser)
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, AudioMessage)

config = configparser.ConfigParser()
config.read('config.ini')
channel_secret = config['LINE']['LINE_CHANNEL_SECRET']
channel_access_token = config['LINE']['LINE_CHANNEL_ACCESS_TOKEN']

app = FastAPI()
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(channel_access_token, async_http_client)
parser = WebhookParser(channel_secret)


@app.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event.message, AudioMessage):
            message_content = await line_bot_api.get_message_content(event.message.id)
            with open('Audio.M4A', 'wb') as fd:
                async for chunk in message_content.iter_content():
                    fd.write(chunk)

            # ## Return message
            # await line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=event.message.text)
            # )
    return 'OK'


@app.get("/")
async def alive():
    return {"message": "Alive"}
