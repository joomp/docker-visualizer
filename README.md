# Docker visualizer

A tool for visualizing the relationships between local Docker Linux container images, containers, and image layers.

The application is run in Docker containers and it visualizes the relationships between Docker images, containers, and layers on the same host. The application is intended to be used with Linux Docker containers.

The application consists out of two components: _frontend_ and _backend_. The backend collects all the information displayed by the frontend. The frontend is a browser application that provides a dashboard and a graph for visualizing the data provided by the backend. The backend provides API documentation at its root URL. For more information about these components, see their respective directories.

## How to run
The recommended way to run the application is with the command: 
```
docker-compose up
```
After the containers are ready, the application is available at http://localhost:8080.

**_NOTE:_**  The backend has specific requirements in order to work as expected. For example, it should be run with privileges, and it should have access to the host Docker UNIX socket. See backend/README.md for more information. The frontend needs the backend API URL defined as a build-time ENV variable. When run with docker-compose, all these configurations are already set.

The application is intended to be run with docker-compose.yml. docker-compose.dev.yml is intended for development and it helps debugging, and provides automatic restart on changes for the backend.

When run with ``docker-compose up`` the application consist out of three containers. The frontend container contains the frontend application. The backend container contains the backend application. The nginx container acts as a reverse proxy for the frontend and the backend applications.

The application does not modify the host system in any way. The application can be removed without leaving a trace, by deleting the application containers, for example with the command ``docker-compose down``.

## Overview
[Screenshots and description]

## Compatibility
Docker supports both Windows and Linux containers, but this application is designed only to be used with Linux containers. Docker can run Linux containers on Windows, Linux, and macOS platforms. The application is developed and tested on Windows 10. In principle, the application should work on other platforms with compatible Docker versions, but they are not tested. 

The application is developed and tested with Docker version 20.10. Docker API used by the Docker SDK is backwards compatible, making the application compatible with Docker versions 20.10 or better. The application is not tested with older Docker versions. The application may work with older Docker versions.

PSS calculation may not work properly under all Docker setups. The application is designed to handle the cases where PSS is not available gracefully.

## Troubleshooting & Issues
If port 8080 is taken, you can change the port by editing nginx port mapping in docker-compose file.

The backend errors are logged to the console. Docker related errors on start-up probably mean that the Docker socket is not available for the container, or Docker daemon is not running.

Rendering large graphs may take a while.
