FROM python:3.8
WORKDIR /app
COPY main.py /app
COPY test.sync.py /app
COPY example.json /app
COPY requirements.txt /app
COPY example.wav /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN pip install torch==1.11.0+cpu torchvision==0.12.0+cpu torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -U openai-whisper
RUN pip install -r requirements.txt
#RUN apt-get install gcc musl-dev python3-dev libffi-dev openssl-dev
RUN pip install --upgrade pip
ENTRYPOINT ["python"]
#CMD ["test.sync.py"]
CMD ["main.py"]
