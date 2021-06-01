import hashlib
import json
import os
import time

import leancloud
from flask import Flask, render_template, request
from flask_cors import CORS

from .__version__ import __version__

app = Flask(__name__)
CORS(app, supports_credentials=True)

LCID = os.environ.get("APPID", default=None)
LCKEY = os.environ.get("APPKEY", default=None)

if not (LCID and LCKEY):
    raise RuntimeError(
        "You should set environment variables `APPID` and `APPKEY` first! "
        "Please read README of repo."
    )

m = hashlib.md5()
m.update((LCID + LCKEY).encode())
CKID = m.hexdigest() + "_usrid"

leancloud.init(LCID, LCKEY)
OrLike = leancloud.Object.extend("OrLike")


def add_version_to_response(response: dict) -> dict:
    response["version"] = f"V{__version__}"

    return response


@app.route("/", methods=["GET"])
def style():
    return render_template("test.html", server="")


@app.route("/tmp", methods=["GET"])
def sdtmp():
    func = request.args.get("callback")

    response = {"stat": "ok", "template": render_template("orlike.html")}
    add_version_to_response(response)

    return func + "(" + json.dumps(response) + ")"


@app.route("/orl", methods=["GET"])
def orl():
    method = request.args.get("method")
    func = request.args.get("callback")
    if method != "like" and method != "dislike":
        return func + "(" + json.dumps({"stat": "failed"}) + ")"

    link = request.args.get("link")
    uid = request.args.get(CKID)

    query = OrLike.query
    query.equal_to("method", method)
    query.equal_to("link", link)
    query.equal_to("uid", uid)
    print(method, link, uid)
    exist = query.find()
    if not exist:
        orlike = OrLike()
        orlike.set("method", method)
        orlike.set("link", link)
        orlike.set("uid", uid)
        orlike.save()
    else:
        [e.destroy() for e in exist]

    response = {"stat": "ok", "uid": uid}
    add_version_to_response(response)

    return func + "(" + json.dumps(response) + ")"


@app.route("/qry", methods=["GET"])
def qry():
    link = request.args.get("link")
    query = OrLike.query
    query.equal_to("method", "like")
    query.equal_to("link", link)
    cnt_like = query.count()
    query.equal_to("method", "dislike")
    query.equal_to("link", link)
    cnt_dislike = query.count()

    func = request.args.get("callback")

    response = {"stat": "ok", "like": cnt_like, "dislike": cnt_dislike}
    add_version_to_response(response)

    return func + "(" + json.dumps(response) + ")"


@app.route("/ckusr", methods=["GET"])
def ckusr():
    response = {"stat": "ok", "ckid": CKID}
    td = str(time.time())
    m = hashlib.md5()
    m.update((td + request.remote_addr).encode())

    func = request.args.get("callback")

    response["uid"] = m.hexdigest()
    add_version_to_response(response)

    return func + "(" + json.dumps(response) + ")"
