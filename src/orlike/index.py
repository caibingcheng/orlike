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


def format_response(request: dict, response: dict, stat: str) -> dict:
    func = request.args.get("callback")
    response["version"] = f"V{__version__}"
    response["stat"] = f"{stat}"
    return f"{func}({json.dumps(response)})" if func else json.dumps(response)


@app.route("/", methods=["GET"])
def demo():
    return render_template("test.html", server="")


@app.route("/tmp", methods=["GET"])
def sdtmp():
    response = {"template": render_template("orlike.html")}

    return format_response(request, response, "ok")


@app.route("/orl", methods=["GET"])
def orl():
    method = request.args.get("method")
    if method not in {"like", "dislike"}:
        response = {"reason": "invalid method"}
        return format_response(request, response, "failed")

    link = request.args.get("link")
    uid = request.args.get(CKID)

    query = OrLike.query
    query.equal_to("method", method)
    query.equal_to("link", link)
    query.equal_to("uid", uid)
    exist = query.find()
    if not exist:
        orlike = OrLike()
        orlike.set("method", method)
        orlike.set("link", link)
        orlike.set("uid", uid)
        orlike.save()
    else:
        [e.destroy() for e in exist]

    response = {"uid": uid}

    return format_response(request, response, "ok")


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

    response = {"like": cnt_like, "dislike": cnt_dislike}

    return format_response(request, response, "ok")


@app.route("/ckusr", methods=["GET"])
def ckusr():
    response = {"stat": "ok", "ckid": CKID}
    td = str(time.time())
    m = hashlib.md5()
    m.update((td + request.remote_addr).encode())

    response["uid"] = m.hexdigest()

    return format_response(request, response, "ok")
