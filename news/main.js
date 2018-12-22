function select(i) {
  $("#" + selected).css("background-color", "white");
  if (selected != i) {
    selected = i;
    $("#" + selected).css("background-color", "#d4d4d4");
  } else {
    show();
  }
}

function show() {
  var p = 10 * page + selected;
  if (selected != -1) {
    $("#passage").load(conf.cdir + "/" + conf.rssbase + "/" + "getxml.php?method=show" + "&type=" + num + "&page=" + p);
    $("#tables").hide();
  }
}

function pageset(i) {
  if (page + i >= 0 && page + i <= 9) {
    page += i;
    selected = -1;
    $("#selections").load(conf.cdir + "/" + conf.rssbase + "/" + "getxml.php?method=table" + "&type=" + num + "&page=" + page);
  }
  pagenum();
}

function pagenum() {
  if (page + 1 < 10) {
    $("#pagenum").html("0" + String(page + 1) + "/10");
  } else {
    $("#pagenum").html(String(page + 1) + "/10");
  }
}

function back() {
  document.getElementById("passage").innerHTML = "";
  $("#tables").show();
}

function switcher() {
  num = (num + 1) % conf.rss.length;
  countryname();
  $("#selections").load(conf.cdir + "/" + conf.rssbase + "/" + "getxml.php?method=table" + "&type=" + num + "&page=0");
  page = 0;
  pagenum();
}

function countryname() {
  $("#switch").html("切换至" + conf.rss[(num + 1) % conf.rss.length].title);
}
var num = 0;
var page = 0;
var selected = -1;
var conf = {};

$.getJSON("config.json").then(function(data) {
  conf = data;
  $("#selections").load(conf.cdir + "/" + conf.rssbase + "/" + "getxml.php?method=table&type=0&page=0");
});