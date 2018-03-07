$("#difficulty").val(sessionStorage.getItem("level"));
$("#rate").val(sessionStorage.getItem("rate"));

var source_lang = sessionStorage.getItem("origin_lang_id");
var target_lang = sessionStorage.getItem("target_lang_id");


$("#source").children("#source-" + source_lang).addClass("active");
$("#target").children("#target-" + target_lang).addClass("active");

//revert state when close without apply
$("button.close").click(function(){
  var current_active = document.getElementsByClassName("active");
  $(current_active).removeClass('active');
  $("#source").children("#source-" + source_lang).addClass("active");
  $("#target").children("#target-" + target_lang).addClass("active");
  $("#difficulty").val(sessionStorage.getItem("level"));
  $("#rate").val(sessionStorage.getItem("rate"));
});
//move active class
$(".not-button").click(function(){
  var section = $(this).parent().attr("id");
  var current_active = document.getElementsByClassName("active");
  var id;
  for(i = 0; i <current_active.length; i++){
    id = $(current_active[i]).attr('id');
    id= id.split("-");
    if(section == id[0]){
      $(current_active[i]).removeClass('active');
    }
  }
  $(this).addClass('active');
});

//increment/decrement buttons
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


