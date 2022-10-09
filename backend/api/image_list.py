"""ImageList

Defines ImageList resource.
"""
from common.docker_client import client
from flasgger import SwaggerView, Schema, fields

class ImageListItemSchema(Schema):
    id = fields.String(required=True)
    tags = fields.List(fields.String, required=True)
    layers = fields.List(fields.String, dump_default=[], attribute='attrs.RootFS.Layers', required=True)

class ImageList(SwaggerView):
    responses = {
        200: {
            'description': 'OK',
            'schema': {
                'type': 'array',
                'items': ImageListItemSchema
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
        """List images
        Returns the list of images on the Docker server.
        Uses a different representation of an image than inspecting a single image. Intermediate image layers are filtered out.
        
        'layers' is an array of layer content hashes, in order from first to last.
        ---
        """
        images = client.images.list()
        return ImageListItemSchema(many=True).dump(images)
    