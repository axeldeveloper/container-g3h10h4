from flask import Flask, render_template, jsonify
from db import get_db, close_db

import sqlalchemy

from logger import log

app = Flask(__name__)
app.teardown_appcontext(close_db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cep")
def get_cep():
    msg = "Buscar cep"
    return jsonify({"status": "success", "message": msg})


@app.route("/company")
def get_company():
    msg = "Buscar companies"
    return jsonify({"status": "success", "message": msg})



@app.route("/health")
def health():
    log.info("Checking /health")
    db = get_db()
    health = "BAD"
    try:
        result = db.execute("SELECT NOW()")
        result = result.one()
        health = "OK"
        log.info(f"/health reported OK including database connection: {result}")
    except sqlalchemy.exc.OperationalError as e:
        msg = f"sqlalchemy.exc.OperationalError: {e}"
        log.error(msg)
    except Exception as e:
        msg = f"Error performing healthcheck: {e}"
        log.error(msg)

    return health
