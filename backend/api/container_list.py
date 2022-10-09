"""ContainerList

Defines ContainerList resource.
"""
from common.docker_client import client
from flasgger import SwaggerView, Schema, fields

class ContainerListItemSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    status = fields.String(required=True)
    image_id = fields.String(attribute='image.id', required=True)
    image_tags = fields.List(fields.String, attribute='image.tags', required=True)

class ContainerList(SwaggerView):
    responses = {
        200: {
            'description': 'OK',
            'schema': {
                'type': 'array',
                'items': ContainerListItemSchema
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                '$ref': '#/definitions/Error'
            }
        }
    }
    
    def get(self):
        """List containers
        Returns the list of containers on the Docker server.
        Uses a different representation of a container than inspecting a single container. All containers are included.
        ---
        """
        containers = client.containers.list(all=True)
        return ContainerListItemSchema(many=True).dump(containers)
    