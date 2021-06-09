import hashlib
import json
import os
import time

import leancloud
from flask import Flask, render_template, request, abort
from flask_cors import CORS
from functools import wraps

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


@app.before_request
def chk_args():
    chk_table = {
        "/": {},
        "/tmp": {},
        "/ckusr": {},
        "/orl": {"method", "link", CKID},
        "/qry": {"link"},
    }

    path = request.path
    func = request.args.get("callback")

    # no args required
    if path not in chk_table.keys():
        response = {"stat": "failed", "message": "invalid url " + path}
        return f"{func}({json.dumps(response)})" if func else json.dumps(response)

    for rq in chk_table[path]:
        if rq not in request.args:
            response = {"stat": "failed", "message": "require " +
                        str(chk_table[path]) + " but get " + json.dumps(request.args)}
            return f"{func}({json.dumps(response)})" if func else json.dumps(response)


def format_response(action_func):
    @wraps(action_func)
    def _format_response(*args, **kwargs):
        response = action_func(*args, **kwargs)
        func = request.args.get("callback")
        response["version"] = f"V{__version__}"
        if "stat" not in response.keys():
            response["stat"] = "ok"
        return f"{func}({json.dumps(response)})" if func else json.dumps(response)
    return _format_response


@app.route("/", methods=["GET"])
def demo():
    return render_template("test.html", server="")


@app.route("/tmp", methods=["GET"])
@format_response
def sdtmp():
    response = {"template": render_template("orlike.html")}

    return response


@app.route("/orl", methods=["GET"])
@format_response
def orl():
    method = request.args.get("method")
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

    return response


@app.route("/qry", methods=["GET"])
@format_response
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

    return response


@app.route("/ckusr", methods=["GET"])
@format_response
def ckusr():
    response = {"ckid": CKID}
    td = str(time.time())
    m = hashlib.md5()
    m.update((td + request.remote_addr).encode())

    response["uid"] = m.hexdigest()

    return response
