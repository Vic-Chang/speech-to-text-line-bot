import aiohttp
import configparser
from fastapi import Request, FastAPI, HTTPException
from linebot import (AsyncLineBotApi, WebhookParser)
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import AudioMessage, TextSendMessage, TextMessage
from pydub import AudioSegment

config = configparser.ConfigParser()
config.read('config.ini')
channel_secret = config['LINE']['LINE_CHANNEL_SECRET']
channel_access_token = config['LINE']['LINE_CHANNEL_ACCESS_TOKEN']

app = FastAPI()
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(channel_access_token, async_http_client)
parser = WebhookParser(channel_secret)


async def process_file():
    pass


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
            file_name = 'Audio.M4A'
            with open(file_name, 'wb') as fd:
                async for chunk in message_content.iter_content():
                    fd.write(chunk)

            request_audio = AudioSegment.from_file(file_name, format="M4A")
            file_handle = request_audio.export(file_name + '.wav', format="wav")
            print(type(file_handle))
            # audio_segment = AudioSegment.from_file(file_name, format="wav")

            # ## Return message
            # await line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=event.message.text)
            # )

    return 'OK'


@app.get("/")
async def alive():
    print('test')
    return {"message": "Alive"}
