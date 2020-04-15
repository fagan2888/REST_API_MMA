FROM python:3.7

RUN mkdir -p /var/app

WORKDIR /var/app

COPY . /var/app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["pytest", "-v", "tests/test_flask_api.py"]

# development
# CMD ["python3", "app.py"]

# production
CMD ["python3", "-m", "flask", "run", "--port=80", "--host=0.0.0.0"]
