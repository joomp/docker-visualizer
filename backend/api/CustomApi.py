'''
CustomApi

Custom class of flask_restful.Api. 
'''
from flask_restful import Api
from flask import jsonify
import docker.errors
import logging


class CustomApi(Api):
    """This class overrides 'handle_error' method of 'flask_restful.Api' class.
    The class extends global exception handing to handle Docker APIErrors.
    """
    def handle_error(self, e):
        if isinstance(e, docker.errors.APIError):
            logging.exception(e)
            message = e.explanation or e.response.reason # explanation can be none
            message = message.capitalize()
            return jsonify({
                    'message': message,
                }), e.status_code
        else: 
            return super().handle_error(e)
        