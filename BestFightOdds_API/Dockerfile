FROM python:3.7.1

RUN mkdir -p /var/BestFightOddsAPI

WORKDIR /var/BestFightOddsAPI

COPY . /var/BestFightOddsAPI

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENTRYPOINT pytest -v /var/BestFightOddsAPI/tests/test_flask_api.py && python /var/BestFightOddsAPI/main.py
