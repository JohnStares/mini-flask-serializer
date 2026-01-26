# Mini Flask Serializer

A lightweight serializer for Flask-SQLAlchemy models with field filtering support. No validation support for now but will be include during future updates.

## Installation

```bash

pip install git+https://github.com/JohnStares/mini-flask-serializer.git

```

## Usage in your flask project

```python

from flask import Flask
from mini_flask_serializer import MiniFlaskSerializer

app = Flask(__name__)

serializer = MiniFlaskSerializer(app)

# Or you can initialize it later

serializer.init_app(app)

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