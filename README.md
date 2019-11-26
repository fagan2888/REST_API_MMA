

If running in the Docker Quickstart Terminal, the Docker terminal is assigned its own IP http://192.168.99.100/. Access the localhost at IP http://192.168.99.100:5000.

Docker commands to run project:

`docker build -f ./Dockerfile -t docker-pkg-name .`

`docker run -p 5000:5000 docker-pkg-name`

There is only a single test file in the directory. 

To run the file with verbosity : `pytest -v test_flask_api.py`. 

To run just the tests that concern the static html pages : `pytest -v test_flask_api.py -m static`.

