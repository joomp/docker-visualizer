"""Resources

Defines importable API.
"""
from .CustomApi import CustomApi

from .container_list import ContainerList
from .container import Container
from .image_list import ImageList
from .image import Image

api = CustomApi(catch_all_404s=True)

api.add_resource(ContainerList, '/containers')
api.add_resource(Container, '/containers/<string:id>')
api.add_resource(Image, '/images/<string:id>')
api.add_resource(ImageList, '/images')
