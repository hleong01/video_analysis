# base python
FROM python:3.9-alpine
MAINTAINER Herman Leong

ENV PORT=8081

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
# install dependencies
RUN apk update
RUN apk add linux-headers make automake gcc g++ subversion python3-dev openblas-dev ffmpeg-libs ffmpeg-dev
RUN pip install -r requirements.txt

COPY . /app
ENTRYPOINT [ "python" ]

CMD [ "realtime_person_detection.py" ]
