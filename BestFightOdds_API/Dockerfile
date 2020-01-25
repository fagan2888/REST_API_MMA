FROM python:3.7.1

RUN mkdir -p /var/best_fight_odds_api

WORKDIR /var/best_fight_odds_api

COPY . /var/best_fight_odds_api

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT pytest -v /var/best_fight_odds_api/tests/test_flask_api.py && python /var/best_fight_odds_api/main.py
