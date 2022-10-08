FROM python:3.10-alpine

ENV TZ=Asia/Taipei

RUN apk update && apk add ffmpeg

WORKDIR /

COPY . /

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80