"""App

Runs the application.
"""
from flask import Flask
from api import api
from swagger import swagger
import os

app = Flask(__name__)
api.init_app(app)
swagger.init_app(app)

if __name__ == '__main__':
    import os
    if os.getenv('PRODUCTION'):
        from waitress import serve
        from paste.translogger import TransLogger
        import logging
        # Enable access logging to the console
        logger = logging.getLogger('waitress')
        logger.setLevel(logging.INFO)

        serve(TransLogger(app, setup_console_handler=False), port=5000)
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
