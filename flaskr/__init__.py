import os

from flask import Flask, render_template


def create_app(test_config=None):
    """Application factory for the Golf Scores app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import scores
    app.register_blueprint(scores.bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
