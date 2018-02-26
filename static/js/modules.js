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
          place_concept_id(instance);
          
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
              target_tag(instance);
            }
            else{
              origin_tag(instance);
            }

            //flipped flag
            $(instance).addClass("flipped");

            //place concept id on the end of the list
            place_concept_id(instance);
            

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

function target_tag(instance){
  $(instance).addClass("spa");
  $(instance).removeClass("eng");
}

function origin_tag(instance){
  $(instance).addClass("eng");
  $(instance).removeClass("spa");
}

function flag_tag(){

}

function place_concept_id(instance){
  $(instance).removeClass(concept_id);
  $(instance).addClass(concept_id);
}