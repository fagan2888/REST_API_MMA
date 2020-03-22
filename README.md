REST API for https://www.bestfightodds.com/.

If running in the Docker Quickstart Terminal, the Docker terminal is assigned its own IP http://192.168.99.100/. Access the localhost at IP http://192.168.99.100:5000.

Docker commands to run project:

`docker build -f ./Dockerfile -t docker-pkg-name .`

`docker run -p 5000:5000 docker-pkg-name`

To do
----
1. Build web interface for REST API hosted on another site where items can be easily searched for.
