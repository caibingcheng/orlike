const htm_ele = '' +
    '<a class="likeit orlike" href="javascript:void(0)">' +
    '<i class="fa fa-thumbs-up" aria-hidden="true"><span>0</span></i>' +
    '</a>' +
    '<a class="dislikeit orlike" href="javascript:void(0)">' +
    '<i class="fa fa-thumbs-down" aria-hidden="true"><span>0</span></i>' +
    '</a>' +
    '';
$(".orlike-box").html(htm_ele);

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
function OrLike({ serverUrl = "" }) {
    this.serverUrl = serverUrl;
    this.init();
    $('.likeit').click({ obj: this }, this.like);
    $('.dislikeit').click({ obj: this }, this.dislike);
}
OrLike.prototype.init = function () {
    server_url = this.serverUrl;
    obj = this;
    $.ajax({
        type: 'GET',
        url: server_url + '/ckusr',
        dataType: 'jsonp',
        jsonp: "callback",
        jsonpCallback: "success",
        success: function (data) {
            if (data.stat == 'ok') {
                if (getCookie(data.ckid)) {
                    setCookie(data.ckid, data.uid, 30);
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
OrLike.prototype.like = function (event) {
    obj = event.data.obj;
    server_url = obj.serverUrl;
    $.ajax({
        type: 'GET',
        url: server_url + '/orl?method=like&link=' + window.location.pathname,
        dataType: 'jsonp',
        jsonp: "callback",
        jsonpCallback: "success",
        success: function () {
            obj.query();
        },
    });
}
OrLike.prototype.dislike = function (event) {
    obj = event.data.obj;
    server_url = obj.serverUrl;
    $.ajax({
        type: 'GET',
        url: server_url + '/orl?method=dislike&link=' + window.location.pathname,
        dataType: 'jsonp',
        jsonp: "callback",
        jsonpCallback: "success",
        success: function () {
            obj.query();
        },
    });
}