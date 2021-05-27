const htm_ele = '' +
    '<a class="likeit orlike" href="javascript:void(0)">' +
    '<i class="fa fa-thumbs-up" aria-hidden="true"><span>0</span></i>' +
    '</a>' +
    '<a class="dislikeit orlike" href="javascript:void(0)">' +
    '<i class="fa fa-thumbs-down" aria-hidden="true"><span>0</span></i>' +
    '</a>' +
    '</div>' +
    '';

document.getElementsByClassName('orlike-box')[0].innerHTML = htm_ele;

function OrLike({ serverUrl = "" }) {
    this.serverUrl = serverUrl;
    this.init();
}
OrLike.prototype.init = function () {
    server_url = this.serverUrl;
    obj = this;
    $.ajax({
        type: 'GET',
        url: server_url + '/ckusr',
        success: function () {
            obj.query();
            document.getElementsByClassName("likeit")[0].addEventListener("click", obj.like);
            document.getElementsByClassName("dislikeit")[0].addEventListener("click", obj.dislike);
        },
    });
}
OrLike.prototype.query = function () {
    server_url = this.serverUrl;
    $.ajax({
        type: 'GET',
        url: server_url + '/qry?link=' + window.location.pathname,
        success: function (data) {
            console.log(data);
            document.getElementsByClassName("likeit")[0].getElementsByTagName('i')[0].getElementsByTagName('span')[0].innerHTML = data['like'];
            document.getElementsByClassName("dislikeit")[0].getElementsByTagName('i')[0].getElementsByTagName('span')[0].innerHTML = data['dislike'];
        },
    });
}
OrLike.prototype.like = function () {
    server_url = this.serverUrl;
    obj = this;
    $.ajax({
        type: 'GET',
        url: server_url + '/orl?method=like&link=' + window.location.pathname,
        success: function () {
            obj.query();
        },
    });
}
OrLike.prototype.dislike = function () {
    server_url = this.serverUrl;
    obj = this;
    $.ajax({
        type: 'GET',
        url: server_url + '/orl?method=dislike&link=' + window.location.pathname,
        success: function () {
            obj.query();
        },
    });
}