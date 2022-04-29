FROM python:3.9

WORKDIR /home/ubuntu/COMP90024/comp90024as2/harvest/harvest_streaming

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "tweet_streaming.py"]