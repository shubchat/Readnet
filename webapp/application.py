import os

from flask import (
    Flask,
    session,
    render_template,
    request,
    session,
    redirect,
    url_for,
    escape,
    flash,
)
from flask_session import Session

# from werkzeug import check_password_hash, generate_password_hash
# from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# import requests
# import os
# import pandas as pd
# import time

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = "random_bytes"
Security_password_salt = "check"


@app.route("/", methods=["GET", "POST"])
def home():
    stories = db.execute(
        "select metadata.bookno,metadata.title,metadata.author,short_stories.content from metadata LEFT JOIN short_stories on metadata.bookno=short_stories.bookno order by random() LIMIT 6"
    ).fetchall()

    return render_template("index.html", story=stories)


@app.route("/recommendations", methods=["GET", "POST"])
def reco():
    bookno = request.form.get("bookno")
    # return bookno

    recos = db.execute(
        "select * from recos where bookno=:bookno", {"bookno": bookno}
    ).fetchone()
    reco1 = db.execute(
        "select metadata.bookno,metadata.title,metadata.author,short_stories.content from metadata LEFT JOIN short_stories on metadata.bookno=short_stories.bookno  where metadata.bookno=:bookno",
        {"bookno": recos.first_reco},
    ).fetchone()
    reco2 = db.execute(
        "select metadata.bookno,metadata.title,metadata.author,short_stories.content from metadata LEFT JOIN short_stories on metadata.bookno=short_stories.bookno  where metadata.bookno=:bookno",
        {"bookno": recos.second_reco},
    ).fetchone()
    reco3 = db.execute(
        "select metadata.bookno,metadata.title,metadata.author,short_stories.content from metadata LEFT JOIN short_stories on metadata.bookno=short_stories.bookno  where metadata.bookno=:bookno",
        {"bookno": recos.third_reco},
    ).fetchone()
    reco4 = db.execute(
        "select metadata.bookno,metadata.title,metadata.author,short_stories.content from metadata LEFT JOIN short_stories on metadata.bookno=short_stories.bookno  where metadata.bookno=:bookno",
        {"bookno": recos.fourth_reco},
    ).fetchone()
    reco5 = db.execute(
        "select metadata.bookno,metadata.title,metadata.author,short_stories.content from metadata LEFT JOIN short_stories on metadata.bookno=short_stories.bookno  where metadata.bookno=:bookno",
        {"bookno": recos.fifth_reco},
    ).fetchone()

    return render_template(
        "recommend.html",
        reco1=reco1,
        reco2=reco2,
        reco3=reco3,
        reco4=reco4,
        reco5=reco5,
    )
    # reco2=db.execute("select * from metadata where bookno=:bookno",{'bookno':recos.second_reco}).fetchone()
    # reco3=db.execute("select * from metadata where bookno=:bookno",{'bookno':recos.third_reco}).fetchone()
    # reco4=db.execute("select * from metadata where bookno=:bookno",{'bookno':recos.fourth_reco}).fetchone()
    # reco5=db.execute("select * from metadata where bookno=:bookno",{'bookno':recos.fifth_reco}).fetchone()
    # return render_template("recommend.html",reco1=reco1,reco2=reco2,reco3=reco3,reco4=reco4,reco5=reco5)

