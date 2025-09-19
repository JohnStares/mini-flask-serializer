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

### In your Flask routes

```python
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(serializer.serialize(user, exclude_fields=['password']))

```