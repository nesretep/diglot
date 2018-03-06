$("#difficulty").val(sessionStorage.getItem("level"));
$("#rate").val(sessionStorage.getItem("rate"));

var source_lang = sessionStorage.getItem("origin_lang_id");
var target_lang = sessionStorage.getItem("target_lang_id");

$("#source_langs").children("#source-" + source_lang).addClass("active");
$("#target_langs").children("#target-" + target_lang).addClass("active");

//buttons
$("#difficulty-button-increment").click(function(){
    var level = $("#difficulty").val();
    level = parseInt(level);
    level++;
    $("#difficulty").val(level);

});
$("#difficulty-button-decrement").click(function(){
    var level = $("#difficulty").val();
    level = parseInt(level);
    level--;
    $("#difficulty").val(level);
});
$("#rate-button-increment").click(function(){
    var rate = $("#rate").val();
    rate = parseInt(rate);
    rate++;
    $("#rate").val(rate);
});
$("#rate-button-decrement").click(function(){
    var rate = $("#rate").val();
    rate = parseInt(rate);
    rate--;
    $("#rate").val(rate);
});



