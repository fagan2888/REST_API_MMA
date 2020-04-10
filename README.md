REST API for https://www.bestfightodds.com/.

If running in the Docker Quickstart Terminal, the Docker terminal is assigned its own IP http://192.168.99.100/. Access the localhost at IP http://192.168.99.100:5000 on a Windows machine, and http://172.17.0.2:5000/ on Linux.

Docker commands to run project:

`docker build -f ./Dockerfile -t docker-pkg-name .`

`docker run -p 5000:5000 docker-pkg-name`

---

Commands to update Postgres database. Reason to use `flask_migrate` is when modifications are made in `manage.py` it will automatically update the Postgres database as well.

1. python manage.py db init
2. python manage.py db migrate
3. python manage.py db upgrade


To do
----
1. Build web interface for REST API hosted on another site where items can be easily searched for.


