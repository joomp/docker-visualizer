"""Docker Client

Provides importable configured Docker SDK client:
    client - Docker client
"""
import docker

client = docker.from_env()
