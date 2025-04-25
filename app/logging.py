
from flask import request


def init_logging(app):
    @app.after_request
    def log_request(response):
        if request.path not in ['/favicon.ico']:
            app.logger.info(
                "{request.remote_addr} - {request.method} {request.path} -"
                "{response.status_code}")
        return response
