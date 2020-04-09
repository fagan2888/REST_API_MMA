FROM python:3.7

RUN mkdir -p /var/app

WORKDIR /var/app

COPY . /var/app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["pytest", "-v", "/var/app/tests/test_flask_api.py"]
CMD ["python", "/var/app/app.py"]
