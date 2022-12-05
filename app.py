from datetime import datetime
from urllib.parse import urlparse
import sqlite3

from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

from decorators import login_required
from db_queries import GET_DATA_BY_URL, GET_DATA_BY_DOMAIN

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_jooble.db"
db = SQLAlchemy(app)


def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as er:
        return False


class EmployeesVisits(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    created_date = db.Column(db.DateTime, default=datetime.now,)
    visit_date = db.Column(db.DateTime, nullable=False,)
    original_url = db.Column(db.String, nullable=False,)
    domain_name = db.Column(db.String(256), nullable=False,)  # max length for domain name can be 253 chars
    final_url = db.Column(db.String, default="",)
    status_code = db.Column(db.Integer, nullable=False,)
    title = db.Column(db.String(256),)

    def __init__(self, visit_date, original_url, domain_name, status_code, title, final_url=""):
        self.visit_date = datetime.strptime(visit_date, DT_FORMAT)
        self.original_url = original_url
        self.domain_name = domain_name
        self.status_code = status_code
        self.title = title
        self.final_url = final_url

    def __repr__(self):
        return f"Visit was created for url {self.original_url}"


@app.route("/api/add_ev", methods=["POST", ])
@login_required
def add_employees_visits():
    req = request.get_json()
    new_ev = EmployeesVisits(**req)

    db.session.add(new_ev)
    db.session.commit()
    return Response(new_ev.title, status=200)

@app.route("/api/get_visit", methods=["POST", ])
def get_visit():
    domain_name = request.json.get("domain_name") if request.content_type == "application/json" else request.form.get("domain_name")
    if not domain_name:
        return Response("Check your args at body, looks like you missed something", status=400)

    if validate_url(domain_name):
        raw_query = GET_DATA_BY_URL
    else:
        raw_query = GET_DATA_BY_DOMAIN

    with db.engine.connect() as cr:
        query_res = cr.execute(raw_query, {"name": domain_name, "dtf": DT_FORMAT})
        fetch = query_res.fetchone()
    if fetch:
        # dummy but worked way to get list from concat string... that was done due to sqlite limitations
        res = dict(fetch._mapping)
        if res.get("url_list"):
            res["url_list"] = res["url_list"].split(',|,')

        return jsonify(res)

    return Response(f"No information about {domain_name=}", status=404)

if __name__ == "__main__":
    app.run(debug=True)

    # Uncomment for create a new db
    # with app.app_context():
    #     db.create_all()
