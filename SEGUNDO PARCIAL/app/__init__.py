import os

from flask import Flask, render_template
from flask_migrate import Migrate
from models import db
from controllers import bp_medicos, bp_pacientes, bp_citas

migrate = Migrate()


def create_app():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    template_dir = os.path.join(root_dir, "templates")

    app = Flask(__name__, template_folder=template_dir)
    app.config.from_mapping(
        SECRET_KEY="dev-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///medicontrol.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def home():
        return render_template("home.html")

    app.register_blueprint(bp_medicos)
    app.register_blueprint(bp_pacientes)
    app.register_blueprint(bp_citas)

    return app
