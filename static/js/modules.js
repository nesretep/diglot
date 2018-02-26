//gets json for manipulation
var chapterJSON = {};
fetch('http://diglot.it.et.byu.edu/eng/1Nephi/01').then((response) => {
  return response.json().then((json) => {
    //console.log("JSON", json)
     chapterJSON = json;
  });
});
//console.log(chapterJSON);



function peek(instance_id){

  //get master position
  var classList = document.getElementById(instance_id).className.split(/\s+/);
  var mp = classList[classList.length-2];

  //get target language
  var instance = document.getElementById(instance_id);
  var id = $(instance).attr('id');;
  id = id.split(":");
  var current_lang = id[0];
  var lang = "spa";
  if(current_lang == "spa"){
    lang = "eng";
  }

  //fetch
  var url = "http://diglot.it.et.byu.edu/peek?lang=" + lang + "&mp=" + mp;
  fetch(url).then((response) => {
    return response.json().then((json) => {
      //console.log("JSON", json)
      var popup = document.getElementById("peek");
      $(popup).text(json["instance_text"]);
      
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
              child.append("<span onClick='APIflip(this)'>Flip</span>");


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


function APIflip_back(e){

  //get the instance id
  var span = $(e).parent().parent();
  span.removeClass("flipped");
  var id = span.attr("id");
  var chunk = span.attr("id");
  var popupChunk = "myPopup" + chunk;

  var word = span.clone().children().remove();
  word = word.end().text().trim();

  var classList = document.getElementById(id).className.split(/\s+/);

  id = id.split(":");
  var lang = "eng";
  var target_lang = "spa";
  var concept_id = classList[classList.length-1];
  var master_position = classList[classList.length-2];

  var url = "http://diglot.it.et.byu.edu/flipback?lang=" + lang + "&target_lang=" + target_lang + "&user_id=1&concept_id=" + concept_id;
  console.log(url);
  fetch(url).then((response) => {
      return response.json().then((json) => {
        //console.log("JSON", json);
        
        //change words
        for(i=0; i < json.length-1; i++){
          var instance = document.getElementById(json[i].target_instance_id);

          $(instance).removeClass("flipped");
          $(instance).addClass("eng");
          $(instance).removeClass("spa");

          //place concept id on the end of the list
          $(instance).removeClass(master_position);
          $(instance).addClass(master_position);
          $(instance).removeClass(concept_id);
          $(instance).addClass(concept_id);
          

          //fade out, text change, id change
          $(instance).fadeOut('fast');
          $(instance).html('&nbsp;');
          $(instance).append(json[i].origin_instance_text);
          $(instance).attr("id", json[i].origin_instance_id);
          $(instance).fadeIn();
        }//end for loop

    });
  });
  //change tags

}
function APIflip(e){
  //get the instance id
    
   var span = $(e).parent().parent();

  if(span.hasClass("flipped")==false){
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
    var master_position = classList[classList.length-2];
    //alert(master_position);
    //get from user preference

    if($(span).hasClass("spa")){
      target_lang = "eng";
    }
    //var new_concept = lang + "_" + concept_id.substring(4);

    var url = "http://diglot.it.et.byu.edu/flip?target_lang=" + target_lang + "&user_id=1&concept_id=" + concept_id;
    console.log(url);
    fetch(url).then((response) => {
        return response.json().then((json) => {
          //console.log("JSON", json);
          
          //change words
          for(i=0; i < json.length-1; i++){
            var instance = document.getElementById(json[i].origin_instance_id);

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
            place_mp_tag(instace);
            place_concept_tag(instance);
            

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
  else{
    APIflip_back(e);
  }
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

function place_mp_tag(instance){
  $(instance).removeClass(master_position);
  $(instance).addClass(master_position);  
}
function place_concept_tag(instance){
  $(instance).removeClass(concept_id);
  $(instance).addClass(concept_id);
}

function place_spa_tag(instance){
  $(instance).addClass("spa");
  $(instance).removeClass("eng");
}
function place_eng_tag(instance){
  $(instance).addClass("eng");
  $(instance).removeClass("spa");
}
