from flask import Flask
from sqlalchemy.engine import URL

db_uri = URL(
    drivername='mysql+pymysql',
    username='invoice_db_user',
    password='An0thrS3crt',
    host='127.0.0.1',
    database='invoice_db',
).render_as_string(hide_password=False)


def create_app(db_uri: str = db_uri):
    app = Flask(__name__)

    from lib.error.errorhandlers import error_handlers
    app.register_blueprint(error_handlers, url_prefix='')

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    from lib.database import db
    db.init_app(app)

    from lib.views import api
    app.register_blueprint(api, url_prefix='')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
