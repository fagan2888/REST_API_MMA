FROM python:3.7.1

RUN mkdir -p /var/docker-restapi

WORKDIR /var/docker-restapi

COPY . /var/docker-restapi

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENTRYPOINT pytest -v /var/docker-restapi/tests/test_flask_api.py && python /var/docker-restapi/main.py
