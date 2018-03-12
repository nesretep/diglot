$("#difficulty").val(sessionStorage.getItem("level") + " %");
$("#rate").val(sessionStorage.getItem("rate"));

var source_lang = sessionStorage.getItem("origin_lang_id");
var target_lang = sessionStorage.getItem("target_lang_id");


//set the selects to user settings
$("select#source").val(source_lang);
$("select#target").val(target_lang);


//revert state when close without apply
$("button.close").click(function(){
  var current_active = document.getElementsByClassName("active");
  $(current_active).removeClass('active');
  $("select#source").val(source_lang);
  $("select#target").val(target_lang);
  $("#difficulty").val(sessionStorage.getItem("level"));
  $("#rate").val(sessionStorage.getItem("rate"));
});

function applySettings(){
  var user_id = sessionStorage.getItem("user_id");
  var origin_lang = document.getElementById("");
  var target_lang;
  var rate;
  var level;

}

