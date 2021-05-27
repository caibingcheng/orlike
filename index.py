from flask import Flask, request, make_response, jsonify
import leancloud
import hashlib
import time

LCID = ""
LCKEY = ""

m = hashlib.md5()
m.update((LCID + LCKEY).encode())
CKID = m.hexdigest() + "_usrid"

app = Flask(__name__)
leancloud.init("hQFfnAHKAPnHTsmX3TOdHF8w-MdYXbMMI", "GKFTEbIuDSQezoogEXDjsUGv")
OrLike = leancloud.Object.extend('OrLike')


@app.route('/orl', methods=["GET"])
def orl():
    method = request.args.get('method')
    if (method != 'like' and method != 'dislike'):
        return make_response("failed")
    link = request.args.get('link')
    uid = request.cookies.get(CKID)

    query = OrLike.query
    query.equal_to('method', method)
    query.equal_to('link', link)
    query.equal_to('uid', uid)
    if not query.find():
        orlike = OrLike()
        orlike.set('method', method)
        orlike.set('link', link)
        orlike.set('uid', uid)
        orlike.save()
    return make_response("success")


@app.route('/qry', methods=["GET"])
def qry():
    link = request.args.get('link')
    query = OrLike.query
    query.equal_to('method', "like")
    query.equal_to('link', link)
    cnt_like = query.count()
    query.equal_to('method', "dislike")
    query.equal_to('link', link)
    cnt_dislike = query.count()
    return make_response(jsonify({'like': cnt_like, 'dislike': cnt_dislike}))


@app.route('/ckusr', methods=["GET"])
def ckusr():
    response = make_response("success")
    if request.cookies.get(CKID) == None:
        td = str(time.time())
        m = hashlib.md5()
        m.update((td + request.remote_addr).encode())
        response.set_cookie(CKID, m.hexdigest(), max_age=(60*60*24*30))
    return response
