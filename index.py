from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import leancloud
import hashlib
import time
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

LCID = ""
LCKEY = ""

m = hashlib.md5()
m.update((LCID + LCKEY).encode())
CKID = m.hexdigest() + "_usrid"

leancloud.init("hQFfnAHKAPnHTsmX3TOdHF8w-MdYXbMMI", "GKFTEbIuDSQezoogEXDjsUGv")
OrLike = leancloud.Object.extend('OrLike')


@app.route('/orl', methods=["GET"])
def orl():
    method = request.args.get('method')
    func = request.args.get('callback')
    if (method != 'like' and method != 'dislike'):
        return func + "(" + json.dumps({'stat': 'failed'}) + ")"
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
    return func + "(" + json.dumps({'stat': 'ok'}) + ")"


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
    response = {'stat': 'ok', 'like': cnt_like, 'dislike': cnt_dislike}
    func = request.args.get('callback')
    return func + "(" + json.dumps(response) + ")"


@app.route('/ckusr', methods=["GET"])
def ckusr():
    response = {'stat': 'ok', 'ckid': CKID}
    if request.cookies.get(CKID) == None:
        td = str(time.time())
        m = hashlib.md5()
        m.update((td + request.remote_addr).encode())
        response['uid'] = m.hexdigest()
    func = request.args.get('callback')
    return func + "(" + json.dumps(response) + ")"
