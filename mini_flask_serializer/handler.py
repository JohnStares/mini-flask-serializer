from flask import Flask, jsonify, Response

from typing import Literal

from mini_flask_serializer.exception import ValidationError, AttributeError

def handle_error(app: Flask):
    """
    This handles the app errors
    
    :param app: Your Flask app
    :type app: Flask
    """
    if not isinstance(app, Flask):
        raise TypeError(f"Expects Flask but got {type(app)} instead")
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error) -> tuple[Response, Literal[400]]:
        return jsonify({
            "type": "ValidationError",
            "error": f"{error}"
        }), 400
    

    @app.errorhandler(AttributeError)
    def handle_attribute_error(error) -> tuple[Response, Literal[400]]:
        return jsonify({
            "type": "AttributeError",
            "error": f"{error}"
        }), 400
    

    @app.errorhandler(Exception)
    def handle_exceptions(error) -> tuple[Response, Literal[500]]:
        return jsonify({
            "type": f"{Exception.__class__.__name__}",
            "error": f"{error}"
        }), 500