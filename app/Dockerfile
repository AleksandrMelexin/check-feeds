FROM python:3.13.1-bullseye

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip -r requirements.txt

COPY . /app

EXPOSE 4000

ENTRYPOINT ["python"]

CMD ["app.py"]