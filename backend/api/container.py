"""Container

Defines Container resource.
"""
from common.docker_client import client
from docker.models.containers import Container as DockerContainer
from flasgger import SwaggerView, Schema, fields
from typing import Optional
from flask_restful import abort
import docker.errors
import psutil
import asyncio
import logging

class Port(Schema):
    ip = fields.String(attribute='IP', required=True, dump_default='')
    private_port = fields.String(attribute='PrivatePort', required=True, dump_default='')
    public_port = fields.String(attribute='PublicPort', required=True, dump_default='')
    type = fields.String(attribute='Type', required=True, dump_default='')
    
class Mount(Schema):
    source = fields.String(attribute='Source', required=True, dump_default='')
    destination = fields.String(attribute='Destination', required=True, dump_default='')
    mode = fields.String(attribute='Mode', required=True, dump_default='')
    type = fields.String(attribute='Type', required=True, dump_default='')

class ContainerSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    status = fields.String(required=True)
    image_id = fields.String(attribute='image.id', required=True)
    
    created = fields.Integer(attribute='df.Created', required=True, dump_default=0)
    graph_driver = fields.String(attribute='attrs.GraphDriver.Name', required=True, dump_default='')
                      
    image = fields.String(attribute='df.Image', required=True, dump_default='')
    command = fields.String(attribute='df.Command', required=True, dump_default='')
    ports = fields.Nested(Port, attribute='df.Ports', many=True, required=True, dump_default=[])
    mounts = fields.Nested(Mount, attribute='df.Mounts', many=True, required=True, dump_default=[])
    size_rw = fields.Integer(attribute='df.SizeRw', required=True, dump_default=0)
    size_rootfs = fields.Integer(attribute='df.SizeRootFs', required=True, dump_default=0)
    status_description = fields.String(attribute='df.Status', required=True, dump_default="")
    
    processes = fields.Integer(attribute='stats.pids_stats.current', required=True, dump_default=0)
    memory_usage = fields.Integer(required=True, dump_default=0)
    pss = fields.Integer(required=True, dump_default=0)

def _get_container(id:str) -> Optional[DockerContainer]:
    """Returns the Docker Container. If cannot find the container returns None.

    Args:
        id (str): container id

    Returns:
        DockerContainer: Container
        None: Could not find the container
    """
    try: 
        return client.containers.get(id)
    except docker.errors.NotFound:
        return None
    
async def _get_container_df(id:str) -> Optional[dict]:
    """Returns the df information on the Docker container. If container is not found returns None.

    Args:
        id (str): container id

    Returns:
        Dict: Dict containing Df information on the container 
        None: Could not find the container
    """
    containers = client.df()['Containers']
    for cont in containers:
        if cont['Id'] == id:
            return cont
    return None

async def _pss(container: DockerContainer) -> int:
    """Returns the PSS memory statistic of the container. On failure returns 0.
    PSS is computed as the sum of the PSS values of the processes in the container.
    Args:
        container (DockerContainer): Target container

    Returns:
        int: PSS of the container
    """
    try:
        # The container parent process PID in host PID namespace
        init_pid = container.attrs['State']['Pid']
        if not init_pid:
            # Container is not running
            return 0
        init = psutil.Process(pid=init_pid)
        pss = init.memory_full_info().pss
        for child in init.children(recursive=True):
            try:
                pss += child.memory_full_info().pss
            except psutil.NoSuchProcess:
                # The child process doesn't exist anymore
                pass
        return pss
    except Exception as e:
        logging.exception(e)
        return 0

class Container(SwaggerView):
    responses = {
        200: {
            'description': 'OK',
            'schema': ContainerSchema,
        },
        404: {
            'description': 'Container not found',
            'schema': {
                '$ref': '#/definitions/Error'
          }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                '$ref': '#/definitions/Error'
            }
        }
    }
    
    def get(self, id):
        """Inspect Container
        
        Get detailed information about a container on the Docker server.
        If container is not running memory_usage and pss(proportional set size) are 0. If pss is not available, it is returned as 0.
        
        'id' can be an container name or an container id. Container id can be partial. If an container is not uniquely identified, or is not found, responses with 404. Responds with 500, if A disk usage operation is already running. 
        
        'pss' is the Proportional set size memory metric for the container. The PSS for a container is computed as a sum of the PSS values of the processes in the container.
        
        'stats.memory_usage' is computed similarly to Docker CLI
        ---
        parameters:
          - name: id
            in: path
            type: string
            description: Container name or id.
            required: true
        """
        async def helper(container: DockerContainer) -> DockerContainer:
            # Using async makes this little faster
            df = _get_container_df(container.id)
            pss = _pss(container)
            if container.status == 'running':
                container.stats = container.stats(stream=False)
                try:
                    # cgroup v1 host
                    container.memory_usage = container.stats['memory_stats']['usage'] - container.stats['memory_stats']['stats']['total_inactive_file']
                except:
                    # cgroup v2 host
                    try:
                        container.memory_usage = container.stats['memory_stats']['usage'] - container.stats['memory_stats']['stats']['inactive_file']
                    except Exception as e:
                        logging.exception(e)
            container.df = await df
            container.pss = await pss
            return container
            
        container = _get_container(id)
        if not container:
            abort(404, message='Container not found.')
        asyncio.run(helper(container))
        return ContainerSchema().dump(container)
    