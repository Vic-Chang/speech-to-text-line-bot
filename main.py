import aiohttp
import configparser
import speech_recognition as sr
from io import BytesIO
from fastapi import Request, FastAPI, HTTPException
from linebot import (AsyncLineBotApi, WebhookParser)
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import AudioMessage, TextSendMessage, MessageEvent
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
        if not isinstance(event, MessageEvent):
            continue

        if isinstance(event.message, AudioMessage):
            message_content = await line_bot_api.get_message_content(event.message.id)

            m4a_audio_bytes_io = BytesIO()
            async for chunk in message_content.iter_content():
                m4a_audio_bytes_io.write(chunk)
            m4a_audio_bytes_io.seek(0)

            request_audio = AudioSegment.from_file(m4a_audio_bytes_io, format="M4A")
            wav_audio_bytes_io = request_audio.export(format="wav")

            r = sr.Recognizer()
            with sr.AudioFile(wav_audio_bytes_io) as source:
                recognizer_audio = r.record(source)

            # Return message
            await line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=r.recognize_google(recognizer_audio, language='zh-TW'))
            )

    return 'OK'


@app.get("/")
async def alive():
    return {"message": "Alive"}
