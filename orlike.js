function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) { return c.substring(name.length, c.length); }
    }
    return "";
}
function OrLike({ serverUrl = "", el = "", days = 30 }) {
    this.serverUrl = serverUrl;
    this.el = el;
    this.days = days;
    this.ckid = "";
    this.init();
}
OrLike.prototype.init = function() {
    server_url = this.serverUrl;
    obj = this;
    $.ajax({
        type: 'GET',
        url: server_url + '/tmp',
        dataType: 'jsonp',
        jsonp: "callback",
        jsonpCallback: "success",
        xhrFields: {
            withCredentials: true
        },
        async: true,
        crossDomain: true,
        success: function (data) {
            $(obj.el).html(data.template);
            obj.ckusr(obj);
            $('.likeit').click({ obj: obj }, obj.like);
            $('.dislikeit').click({ obj: obj }, obj.dislike);
        },
    });
}
OrLike.prototype.ckusr = function (obj) {
    server_url = this.serverUrl;
    $.ajax({
        type: 'GET',
        url: server_url + '/ckusr',
        dataType: 'jsonp',
        jsonp: "callback",
        jsonpCallback: "success",
        xhrFields: {
            withCredentials: true
        },
        async: false,
        crossDomain: true,
        success: function (data) {
            if (data.stat == 'ok') {
                obj.ckid = data.ckid;
                if (!getCookie(data.ckid)) {
                    setCookie(data.ckid, data.uid, obj.days);
                }
                obj.query();
            }
            else {
                console.error('connect orlike failed!!!');
            }
        },
    });
}
OrLike.prototype.query = function () {
    server_url = this.serverUrl;
    $.ajax({
        type: 'GET',
        url: server_url + '/qry?link=' + window.location.pathname,
        dataType: 'jsonp',
        jsonp: "callback",
        jsonpCallback: "success",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        success: function (data) {
            if (data.stat == 'ok') {
                $('.likeit i span').text(data['like']);
                $('.dislikeit i span').text(data['dislike']);
            }
            else {
                console.error('query orlike failed!!!');
            }
        },
    });
}
OrLike.prototype.orl = function (obj, method) {
    server_url = obj.serverUrl;
    req_url = server_url + '/orl?method=' + method + '&link=' + window.location.pathname + '&' + obj.ckid + '=' + getCookie(obj.ckid);
    $.ajax({
        type: 'GET',
        url: req_url,
        dataType: 'jsonp',
        jsonp: "callback",
        jsonpCallback: "success",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        success: function (data) {
            obj.query();
        },
    });
}
OrLike.prototype.like = function (event) {
    obj = event.data.obj;
    obj.orl(obj, 'like');
}
OrLike.prototype.dislike = function (event) {
    obj = event.data.obj;
    obj.orl(obj, 'dislike');
}
