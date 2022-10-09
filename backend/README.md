# Backend
Provides a small and simple HTTP REST-like API for fetching data about Docker objects on the server. All operations in the API are safe and idempotent. Swagger UI API documentation is available at the root URL.

This API is specifically designed for the associated frontend that visualizes the information provided by this API.

Information about the Docker objects is accessed with Docker Python SDK from the Docker Engine whose socket is available for the application. The values returned by the API are similar to the values of Docker API. The PSS value for a container is computed by inspecting the memory usage of the processes in the container. The PSS value is obtained from the shared host operating system running the containers using psutil package.

The application is designed to be used only with Docker Linux containers. The application will not work as expected when run with Docker Windows containers.

API operations and resources are defined in /api/ directory. The application entrypoint is /app.py file.

## Tools
- API is implemented with [Flask](https://palletsprojects.com/p/flask/) and [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/).
- API documentation is generated with [Flasgger](https://github.com/flasgger/flasgger) utilizing [Marshmallow](https://marshmallow.readthedocs.io/) schemas.
- Information about Docker objects is accessed with official[ Docker Python SDK](https://docker-py.readthedocs.io/en/stable/).
- PSS (Proportional set size) for containers is calculated utilizing [psutil](https://psutil.readthedocs.io/en/latest/). 

## API documentation
Swagger UI API documentation is available at the root URL. The documentation is automatically generated with Flasgger.

## How to run

Recommended to be run with the docker-compose files in the repository root directory. The application should always be run in a Docker container.

In order to work properly must:
- have access to the Docker socket for Docker Python SDK.
- have privileges for PSS calculation to work as expected.
- use Docker host PID namespace for PSS calculation to work as expected.

These requirements are configured in the docker-compose files. docker-compose.dev.yml is intended for development and it supports debugging and automatic restarting. docker-compose.yml is intended for all other uses.

## Compatibility
Docker supports both Windows and Linux containers, but this application is designed only to be used with Linux containers. Docker can run Linux containers on Windows, Linux, and macOS platforms. The application is developed and tested on Windows 10. In principle, the application should work on other platforms with compatible Docker versions, but they are not tested. 

The application is developed and tested with Docker version 20.10. Docker API used by the Docker SDK is backwards compatible, making the application compatible with Docker versions 20.10 or better. The application is not tested with older Docker versions. The application may work with older Docker versions.

PSS calculation may not work properly under all Docker setups. The application is designed to handle the cases where PSS is not available gracefully.

## Troubleshooting
Errors are logged to the console. Docker related errors on start-up probably mean that the Docker socket is not available for the container.
