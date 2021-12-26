import os

from flask import Flask

def create_app(test_config=None):
    
    # create and configure the app
    
    app = Flask(__name__, instance_relative_config=True)
    os.environ['FIREBIRD_LOCK'] = '/tmp/test'
    os.environ['FIREBIRD'] = os.path.join(app.root_path, 'rdb')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'KURS_UD.FDB'),
        #DATABASE='/tmp/flaskr.fdb',
        USER='sysdba',
        PASSWORD='asdasd',
        LIBRARY=os.path.join(app.root_path, 'rdb/libfbclient.so')
        #LIBRARY='/opt/RedDatabase/lib/libfbclient.so'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    
    from . import auth
    app.register_blueprint(auth.bp)

    #from . import blog
    #app.register_blueprint(blog.bp)
    #app.add_url_rule('/', endpoint='index')

    from . import student
    app.register_blueprint(student.bp)

    from . import teacher
    app.register_blueprint(teacher.bp)
    
    from . import admin
    app.register_blueprint(admin.bp)


    return app