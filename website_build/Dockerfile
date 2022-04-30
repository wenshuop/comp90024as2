FROM python:3.8
   EXPOSE 5000
   WORKDIR /website_build
　　ADD . /website_build
   RUN pip install -r requirements.txt
   CMD ["python3","app.py"]
