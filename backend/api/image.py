"""Image

Defines Image resource.
"""
from common.docker_client import client
from docker.models.images import Image as DockerImage
import docker.errors
from flasgger import SwaggerView, Schema, fields
from typing import Optional
from flask_restful import abort

class History(Schema):
    created = fields.Integer(dump_default='', attribute='Created', required=True)
    created_by = fields.String(dump_default='', attribute='CreatedBy', required=True)
    size = fields.Integer(dump_default=0, attribute='Size', required=True)

class ImageSchema(Schema):
    id = fields.String(required=True)
    tags = fields.List(fields.String, required=True)
    
    created = fields.Integer(dump_default='', attribute='df.Created', required=True)
    history = fields.Nested(History, many=True, required=True)
    author = fields.String(dump_default='', attribute='attrs.Author', required=True)
    architecture = fields.String(dump_default='', attribute='attrs.Architecture', required=True)
    os = fields.String(dump_default='', attribute='attrs.Os', required=True)
    
    containers = fields.Integer(dump_default=0, attribute='df.Containers', required=True)
    shared_size = fields.Integer(dump_default=0, attribute='df.SharedSize', required=True)
    size = fields.Integer(dump_default=0, attribute='df.Size', required=True)

def _get_image_df(id:str) -> Optional[dict]:
    """Returns the df information on the Docker image.

    Args:
        id (str): image id

    Returns:
        Dict: Dict containing Df information on the image 
    """
    images = client.df()['Images']
    for img in images:
        if img['Id'] == id:
            return img
    return None
    

def _get_image(id:str) -> Optional[DockerImage]:
    """Returns the Docker image. If cannot find the image returns None.

    Args:
        id (str): image id

    Returns:
        DockerImage: Image
        None: Could not find the image
    """
    try: 
        return client.images.get(id)
    except docker.errors.ImageNotFound:
        return None
            
class Image(SwaggerView):
    responses = {
        200: {
            'description': 'OK',
            'schema': ImageSchema,
        },
        404: {
            'description': 'Image not found',
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
        """Inspect image
        Get detailed information about an image on the Docker server.
        
        'id' can be an image name or an image id. Image id can be partial. 'id' may or may not include encryption method. If an image is not uniquely identified, or is not found, responses with 404. Responds with 500, if a disk usage operation is already running. 
                
        'history' is ordered from from first to last.
        'shared_size': is the amount of space that an image shares with another image.
        'size' is the virtual size of the image, it is the sum of shared_size and unique size, where unique size is the amount of space that is only used by a given image.
        ---
        parameters:
          - name: id
            in: path
            type: string
            description: Image name or id.
            required: true
        """
        image = _get_image(id)
        if not image:
            abort(404, message='Image not found.')
        image.history = image.history()
        image.df = _get_image_df(image.id)
        return ImageSchema().dump(image)
