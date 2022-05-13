# Team 13, Melbourne
# Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
# Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
# Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
# Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
# Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au

FROM python:3.8

WORKDIR /home/ubuntu/COMP90024/comp90024as2/website_build

COPY . .

RUN pip install -r requirements.txt

CMD ["python","app.py"]
