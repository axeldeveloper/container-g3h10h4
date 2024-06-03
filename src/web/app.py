import json
import requests
from flask import Flask, render_template, jsonify
from db import DB_SEVER, get_db, close_db

import sqlalchemy

from logger import log

app = Flask(__name__)
app.teardown_appcontext(close_db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("index.html")


@app.route("/consulta")
def consulta():
    return render_template("consulta.html")


@app.route('/consulta/<q_data>', methods=['GET'])
def consultav1(q_data):
    lst_enderecos = []
    resultado = requests.get("https://www.receitaws.com.br/v1/cnpj/" + str(q_data))
    data_endereco = json.loads(resultado.content)
    lst_enderecos.append([
        q_data,
        data_endereco['logradouro'],
        data_endereco['numero'],
        data_endereco['municipio'],
        data_endereco['bairro'],
        data_endereco['uf'], 
        data_endereco['cep'].replace('.', '').replace('-',''),
        resultado
    ])
    print(data_endereco)

    return render_template("company_data.html", context=data_endereco)


@app.route("/cep")
def get_cep():
    msg = "Buscar cep"
    return jsonify({"status": "success", "message": msg})


@app.route("/company")
def get_company():
    msg = "Buscar companies"
    return jsonify({"status": "success", "message": msg})


@app.route("/info")
def get_info():
    msg = DB_SEVER
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
        log.info(f"/health reported OK including db connection: {result}")
    except sqlalchemy.exc.OperationalError as e:
        msg = f"sqlalchemy.exc.OperationalError: {e}"
        log.error(msg)
    except Exception as e:
        msg = f"Error performing healthcheck: {e}"
        log.error(msg)

    return health
