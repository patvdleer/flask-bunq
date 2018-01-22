# flask-bunq
Flask-Bunq wrapper for banking API 

## Installation
PIP not supported (yet)

## Config
Add the following to your config
```python
BUNQ_API_KEY = "YOUR_API_KEY"
BUNQ_API_SANDBOX = False
BUNQ_API_IDENTIFIER = "FLASK_BUNQ"
```

## Usage via extensions

main run
```python

from . import extensions as ext

def init(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    configure_extensions(app)
    
def configure_extensions(app):
    """Configure Flask extensions."""
    ext.bunq.init_app(app)
```

extensions.py
```python
from flask_bunq import FlaskBunq
bunq = FlaskBunq()
```


Controller/endpoint/viewpoint/w.e.
```python
from flask import Blueprint
from YOURAPP.extensions import bunq

example = Blueprint('example', __name__)

@example.route('/test')
def test():
    
    api_context = bunq.context
    users = endpoint.User.list(api_context).value

```
