REST API for https://www.bestfightodds.com/.

If running in the Docker Quickstart Terminal, the Docker terminal is assigned its own IP http://192.168.99.100/. Access the localhost at IP http://192.168.99.100:5000 on a Windows machine, and http://172.17.0.2:5000/ on Linux.

** If you're running a VPN, you won't be able to access the docker container via the container IP.

Docker commands to run project:

`docker build -f ./Dockerfile -t docker-pkg-name .`

`docker run -p 5000:5000 docker-pkg-name`

Docker command using docker-compose:

`docker-compose up`

---

Commands to update Postgres database. Reason to use `flask_migrate` is when modifications are made in `manage.py` it will automatically update the Postgres database as well.

1. python manage.py db init
2. python manage.py db migrate
3. python manage.py db upgrade

---

Pushing to Docker and the Docker image to AWS ECR
---
1. docker tag mma_rest_api:latest ACCT_ID.dkr.ecr.us-east-1.amazonaws.com/
2. docker push mma_rest_api:latest ACCT_ID.dkr.ecr.us-east-1.amazonaws.com/

ACCT_ID = AWS account ID


Follow this tutorial: https://linuxacademy.com/blog/linux-academy/deploying-a-containerized-flask-application-with-aws-ecs-and-docker/


To do
----
1. Build web interface for REST API hosted on another site where items can be easily searched for.


