import hashlib
import json
import os
import time

import leancloud
from flask import Flask, render_template, request
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
OLCounts = leancloud.Object.extend("OLCounts")


@app.before_request
def chk_args():
    chk_table = {
        "/": {},
        "/tmp": {},
        "/ckusr": {},
        "/orl": {"method", "link", CKID},
        "/qry": {"link"},
        "/topk": {"method", "k"},
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


def qry_cnt_from_orlike(link: str):
    query = OrLike.query
    query.equal_to("method", "like")
    query.equal_to("link", link)
    cnt_like = query.count()

    query.equal_to("method", "dislike")
    query.equal_to("link", link)
    cnt_dislike = query.count()

    return cnt_like, cnt_dislike


def qry_cnt_from_olcounts(link: str):
    cnt_like, cnt_dislike = 0, 0
    query = OLCounts.query
    query.equal_to("link", link)
    cnt = None

    # first有点问题, 没有会触发一个raise
    try:
        # 如果在olcounts里面没有找到, 那么就先从orlike更新olcounts
        # 作为初始化
        cnt = query.first()
        cnt_like, cnt_dislike = cnt.get("like"), cnt.get("dislike")
    except:
        # 从orlike获取不同method的counts
        cnt_like, cnt_dislike = qry_cnt_from_orlike(link)

        if cnt_like > 0 or cnt_dislike > 0:
            # 更新olcounts
            olcounts = OLCounts()
            olcounts.set("link", link)
            olcounts.set("like", cnt_like)
            olcounts.set("dislike", cnt_dislike)
            olcounts.save()
    return cnt, cnt_like, cnt_dislike


@app.route("/orl", methods=["GET"])
@format_response
def orl():
    method = request.args.get("method")
    link = request.args.get("link")
    uid = request.args.get(CKID)
    response = {"uid": uid}

    query = OrLike.query
    query.equal_to("method", method)
    query.equal_to("link", link)
    query.equal_to("uid", uid)

    # first有点问题, 没有会触发一个raise
    try:
        # 如果这条数据存在, 则说明用户是二次点击, 则取消
        # 如果不存在, 则用户是第一次点击, 允许
        exist = query.first()
        exist.destroy()
    except:
        orlike = OrLike()
        orlike.set("method", method)
        orlike.set("link", link)
        orlike.set("uid", uid)
        orlike.save()

    # orl请求也相当于会执行一个qry请求
    # TODO: 能否减少请求次数
    cnt, response["like"], response["dislike"] = qry_cnt_from_olcounts(link)
    # 如果没有qry到, 则说明这是一条新数据, 下面就不需要更新了
    if cnt:
        inc = -1 if exist else 1
        # 如果这条数据存在, 则说明用户是二次点击, 则取消
        # 如果不存在, 则用户是第一次点击, 允许
        cnt.increase(method, inc)
        response[method] += inc
        cnt.save()

    return response


@app.route("/qry", methods=["GET"])
@format_response
def qry():
    link = request.args.get("link")
    cnt, cnt_like, cnt_dislike = qry_cnt_from_olcounts(link)
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


@app.route("/topk", methods=["GET"])
@format_response
def topk():
    method = request.args.get("method")
    k = request.args.get("k")
    query = OLCounts.query
    query.descending(method)
    query.limit(int(k))
    fq = query.find()

    response = {"topk": [{"link": q.get("link"), "cnt": q.get(method)} for q in fq]}

    return response
