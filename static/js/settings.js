$("#difficulty").val(sessionStorage.getItem("level"));
$("#rate").val(sessionStorage.getItem("rate"));

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