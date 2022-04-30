FROM python:3.8
   EXPOSE 5000
   WORKDIR /website_build
　　COPY . .
   RUN pip install -r requirements.txt
   RUN sed -i 's/itervalues/values/g' /usr/local/lib/python3.8/site-packages/flaskext/couchdb.py
   CMD ["python3","app.py"]
