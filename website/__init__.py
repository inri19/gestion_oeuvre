from flask import Flask

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'oeuvre_gestion'

    from .views import views
    from .manage import manage

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(manage, url_prefix='/')

    return app

