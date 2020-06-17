from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

cache = Cache()

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)




from views import *

if __name__ == '__main__':
    app.run(debug=True)