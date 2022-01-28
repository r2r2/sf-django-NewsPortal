FROM python:3.10.2
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/news
COPY requirements.txt ./
RUN pip install -r requirements.txt
