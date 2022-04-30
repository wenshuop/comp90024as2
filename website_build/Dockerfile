FROM python:3.8
   ENV http_proxy http://wwwproxy.unimelb.edu.au:8000/
   ENV https_proxy http://wwwproxy.unimelb.edu.au:8000/
   ENV HTTP_PROXY http://wwwproxy.unimelb.edu.au:8000/
   ENV HTTPS_PROXY http://wwwproxy.unimelb.edu.au:8000/
   EXPOSE 5000
   ENV no_proxy localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.u nimelb.edu.au,.cloud.unimelb.edu.au
   WORKDIR /website_build
　　ADD . /website_build
   RUN pip install -r requirements.txt
   CMD ["python3","app.py"]
