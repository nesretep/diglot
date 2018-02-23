//gets json for manipulation
var chapterJSON = {};
var get = "";
fetch('http://diglot.it.et.byu.edu/eng/1Nephi/01').then((response) => {
  return response.json().then((json) => {
    console.log("JSON", json)
     chapterJSON = json;
  });
});
//console.log(chapterJSON);

function flip_the_phrase3(e){
       //use id to query DB. print result to span        
       var span = $(e).parent().parent();
       var chunk = span.attr("id");
       //window.alert(chunk);
       var popupChunk = "myPopup" + chunk;
       //window.alert(chunk);
       var word = span.clone().children().remove();
       word = word.end().text().trim();
       //window.alert(word);
       var dict = {
              chunk1_eng: "I", chunk1_target: " Yo",
              chunk2_eng: ",", chunk2_target: " ,",
              chunk3_eng: "Nephi", chunk3_target: " Nefi",
              chunk4_eng: ",", chunk4_target: " ,",
              chunk5_eng: "having been born", chunk5_target: " nací",
              chunk6_eng: "of", chunk6_target: " de",
              chunk7_eng: "goodly", chunk7_target: " buenos",
              chunk8_eng: "parents", chunk8_target: " padres",
              chunk9_eng: ",", chunk9_target: " ",
              chunk10_eng: "therefore", chunk10_target: " por tanto",
              chunk11_eng: "I was taught", chunk11_target: " recibí",
              chunk12_eng: "somewhat", chunk12_target: " alguna instrucción",
              chunk13_eng: "in", chunk13_target: " en",
              chunk14_eng: "all", chunk14_target: " toda",
              chunk15_eng: "the learning", chunk15_target: " la ciencia",
              chunk16_eng: "of", chunk16_target: " de",
              chunk17_eng: "my father", chunk17_target: " mi padre",
              chunk18_eng: ";", chunk18_target: " ;",
              chunk19_eng: "and", chunk19_target: " y",
              chunk20_eng: "having seen", chunk20_target: " habiendo conocido",
              chunk21_eng: "many", chunk21_target: " muchas",
              chunk22_eng: "afflictions", chunk22_target: " aflicciones",
              chunk23_eng: "in", chunk23_target: " durante",
              chunk24_eng: "the course", chunk24_target: " el curso",
              chunk25_eng: "of", chunk25_target: " de",
              chunk26_eng: "my days", chunk26_target: " mi vida",
              chunk27_eng: ",", chunk27_target: " ,",
              chunk28_eng: "nevertheless", chunk28_target: " no obstante",
              chunk29_eng: ",", chunk29_target: " ,",
              chunk30_eng: "having been", chunk30_target: " siendo",
              chunk31_eng: "highly", chunk31_target: " altamente",
              chunk32_eng: "favored", chunk32_target: " favorecido",
              chunk33_eng: "of", chunk33_target: " del",
              chunk34_eng: "the Lord", chunk34_target: " Señor",
              chunk35_eng: "in", chunk35_target: " ",
              chunk36_eng: "all", chunk36_target: " todos",
              chunk37_eng: "my days", chunk37_target: " mis dias",
              chunk38_eng: ";", chunk38_target: " ;",
              chunk39_eng: "yea", chunk39_target: " sí",
              chunk40_eng: ",", chunk40_target: " ,",
              chunk41_eng: "having had", chunk41_target: " habiendo logrado",
              chunk42_eng: "a", chunk42_target: " un",
              chunk43_eng: "great", chunk43_target: " grande",
              chunk44_eng: "knowledge", chunk44_target: " conocimiento",
              chunk45_eng: "of", chunk45_target: " de",
              chunk46_eng: "the goodness", chunk46_target: " la bondad",
              chunk47_eng: "and", chunk47_target: " y",
              chunk48_eng: "the mysteries", chunk48_target: " los misterios",
              chunk49_eng: "of", chunk49_target: " de",
              chunk50_eng: "God", chunk50_target: " Dios",
              chunk51_eng: ",", chunk51_target: " ,",
              chunk52_eng: "therefore", chunk52_target: " por tanto",
              chunk53_eng: "I make", chunk53_target: " escribo",
              chunk54_eng: "a record", chunk54_target: " la historia",
              chunk55_eng: "of", chunk55_target: " de",
              chunk56_eng: "my proceedings", chunk56_target: " los hechos",
              chunk57_eng: "in", chunk57_target: " de",
              chunk58_eng: "my days", chunk58_target: " mi vida",
              chunk59_eng: ".", chunk59_target: " ."
       }
       var lookup_value_eng = chunk + "_eng";
       var lookup_value_target = chunk + "_target";
       if(word == dict[lookup_value_eng]){
              span.fadeOut('fast', function(){
              span.text(" " + dict[lookup_value_target]);
              });
              span.fadeIn();
       }
       else{
              span.fadeOut('fast', function(){
              span.text(" " + dict[lookup_value_eng]);
              });
              span.fadeIn();
       }   
}

function defineVue(){
       //get element that fired event, then get it's grandparent (the chunk value)
       if($(event.target.id).parent().attr('id') == "myPopupchunk22"){
              document.getElementById("vs19side").innerHTML = "n. a state of pain, distress,or grief; misery ";
              var side = document.getElementById("vs19side");
              $(side).append('<a class= "glyphicon glyphicon-volume-up" onclick="playMusic();"></a>');  
       }
       else{
              document.getElementById("vs19side").innerHTML = "Define the phrase or word here from " + $(e).parent().attr("id");
       }
}

function peek(instance_id){
  var mp = "";
  var position = 0;
  //iterate through array of JSON to get master position
  for(i = 0; i < chapterJSON.length-1; i++){
    if(chapterJSON[i].instance_id == instance_id){
      mp= chapterJSON[i].master_position;
      position = i;
      break;
    }
  }
  //alert(position);
  var lang = "spa";
 
  var url = "http://diglot.it.et.byu.edu/peek?lang=" + lang + "&mp=" + mp;
  
 
  fetch(url).then((response) => {
    return response.json().then((json) => {
      //console.log("JSON", json)
      var helper = document.getElementById("peek");
      $(helper).text(json["instance_text"]);
      
    });
  });
  
  
}
function popupVue() {

       var alreadyPopup = document.getElementsByClassName("popuptext");
       var exists = $(event.target).children().attr("id");
       var chunk = $(event.target).attr("id");
       //alert(chunk);
       if($(alreadyPopup).attr('id') != null){
              $(alreadyPopup).remove();
       }
       if(chunk == null){
              //do nothing
              //this is in case users click on an area that is not a valid chunk
       }
       else if(exists == null){
              var span = $(event.target);
              span.append("<span class='popuptext' id='myPopup" + chunk + "'></span>");
              var child = span.children();
              
              child.append(" <span id='peek'></span> ");
              child.append(" <br>"); /*or " | "*/
              child.append("<span onclick='APIflip(this)'>Flip</span>");


              var popupChunk = "myPopup" + chunk;
              var popup = document.getElementById(popupChunk);
              popup.classList.toggle("show");
              peek(chunk);
       }
       else{
              var span = $(event.target);
              span.children().remove();
       }
}

function APIflip(e){
  //get the instance id
  var span = $(e).parent().parent();
  var id = span.attr("id");
  var chunk = span.attr("id");
  var popupChunk = "myPopup" + chunk;
  //window.alert(chunk);
  var word = span.clone().children().remove();
  word = word.end().text().trim();

  var classList = document.getElementById(id).className.split(/\s+/);

  id = id.split(":");
  var lang = id[0];
  var book = "1Nephi";
  var chapter = id[2];
  var verse = id[3];
  var pos = id[4];
  var target_lang = "spa";
  var concept_id = classList[classList.length-1];
  //get from user preference

  if($(span).hasClass("spa")){
    target_lang = "eng";
  }
  //var new_concept = lang + "_" + concept_id.substring(4);

  var url = "http://diglot.it.et.byu.edu/flip?target_lang=" + target_lang + "&user_id=1&concept_id=" + concept_id;
  console.log(url);
  fetch(url).then((response) => {
      return response.json().then((json) => {
        console.log("JSON", json);
        
        //change words
        for(i=0; i < json.length-1; i++){
          var instance = document.getElementById(json[i].origin_instance_id);
          //alert(json[i].origin_instance_id);
          //change language class tag
          if(target_lang == "spa"){
            $(instance).addClass("spa");
            $(instance).removeClass("eng");
          }
          else{
            $(instance).addClass("eng");
            $(instance).removeClass("spa");
          }

          //flipped flag
          $(instance).addClass("flipped");

          //place concept id on the end of the list
          $(instance).removeClass(concept_id);
          $(instance).addClass(concept_id);
          

          //fade out, text change, id change
          $(instance).fadeOut('fast');
          $(instance).html('&nbsp;');
          $(instance).append(json[i].target_instance_text);
          $(instance).attr("id", json[i].target_instance_id);
          $(instance).fadeIn();
        }//end for loop

        //append to json
        for(i=0; i < json.length-1; i++){
          for(j = 0; j < chapterJSON.length-1; j++){
            if(chapterJSON[i].instance_id == json[i].origin_instance_id){
              alert("match!");
              chapterJSON[i].target_instance_id = json[i].target_instance_id;
            }
          }
        }//end append loop
        console.log(chapterJSON);

    });
  });
  //change tags
 
}

function APIuser_load(user_id){
  var url = "diglot.it.et.byu.edu/flip?user_id=1";
}

function APIget_flipped_words(){
  //get JSON
  //var url = "http://diglot.it.et.byu.edu/flip?lang=" + lang + "&book=" + book + "&chapter=" + chapter + "&verse=" + verse + "&pos=" + pos + "&target_lang=" + target_lang + "&user_id=1";
  /*fetch(url).then((response) => {
      return response.json().then((json) => {
        //console.log("JSON", json)
    });
  });
  //for loop through json
  for(json){
    span =getelementbyid(json[instance_id])
    span.text = json[instance_text];
    span.id = json[spanish instance id]
  }
  */

}

