FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /blog
COPY requirements.txt /blog/
RUN pip install -r requirements.txt
COPY . /blog/
