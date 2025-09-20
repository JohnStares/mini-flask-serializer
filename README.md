# Mini Flask Serializer

A lightweight serializer for Flask-SQLAlchemy models with field filtering support. No validation support for now but will be include during future updates.

## Installation

```bash

pip install git+https://github.com/JohnStares/mini-flask-serializer.git

```

## Usage in your flask project

```python

from mini_flask_serializer import MiniFlaskSerializer

serializer = MiniFlaskSerializer()

```

### A MUST

create an exception.py file in the same directory your __init__.py file is and do the following.

```python

from mini_flask_serializer.exception import ValidationError

class CustomValidation(ValidationError):
    pass

```


In your __init__.py file where your app = Flask(__name__) do the following.

```python
from flask  import Flask
from .exception import CustomValidationError

def create_app():
    app = Flask(__name__)

    @app.errorhandler(CustomValidationError)
    def handle_validaton_error(error):
        return jsonify({
            "type": "ValidationError",
            "error": f"{error}"
        }), 400


    return app
```

### In your Flask routes

```python
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(serializer.serialize(user, exclude_fields=['password']))

```


```python
from flask import Blueprint, jsonify, request
from mini_flask_serializer import MiniFlaskSerializer
from .exception import CustomValidationError

bp = Blueprint("bp", __name__)

serializers = MiniFlaskSerializer()

@bp.route("/test", methods=["GET", "POST"])
def field_check():
    if request.method == 'POST':
        try:
            serializers.validate_data(fields=request.get_json(), expected_fields=["title", "author", "content"])

            serializers.save_to_model(Book, db)

            return jsonify(serializers.serialize)
    
        except CustomValidationError as e:
            raise e
        except Exception as e:
            return jsonify({"error": str(e)}), 500
```