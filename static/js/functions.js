function peek(instance_id){
  //get master position
  var classList = document.getElementById(instance_id).className.split(/\s+/);
  var mp = classList[classList.length-2];

  //get current language from id
  var chunk = document.getElementById(instance_id);
  var id = $(chunk).attr('id');;
  id = id.split(":");
  var current_lang = id[0];

  //get target language logic
  var target_lang = sessionStorage.getItem("target_lang_id");
  var origin_lang = sessionStorage.getItem("origin_lang_id");
  var lang = target_lang;
  if(current_lang == target_lang){
    lang = origin_lang;
  }
  

  //fetch
  var url = "http://diglot.it.et.byu.edu/peek?lang=" + lang + "&mp=" + mp;
  fetch(url).then((response) => {
    return response.json().then((json) => {
      //put text in pop up
      if(json == null){
        var helper = document.getElementById("peek");
        $(helper).text("No target language match");
        $(helper).attr("id", "peekNone");
      }
      else{
        var helper = document.getElementById("peek");
        $(helper).text(json["instance_text"]);
      }
      
    });
  }); 
}
function popupVue(){
  var alreadyPopup = document.getElementsByClassName("popuptext");
  var exists = $(event.target).children().attr("id");
  var chunk = $(event.target).attr("id");

  //if there is already a pop up, remove it
  if($(alreadyPopup).attr('id') != null){
    $(alreadyPopup).remove();
  }
  if(chunk == "peek"){

  }
  //pop up logic
  else if(chunk == null){
    //do nothing
    //this is in case users click on an area that is not a valid chunk
  }
  else if(exists == null){
    var span = $(event.target);
    span.append("<span class='popuptext' onClick='APIflipnew(this)' id='myPopup" + chunk + "'></span>");
    var child = span.children();

    child.append(" <span id='peek'></span> ");
    //child.append(" <span onClick='APIflip(this)' id='peek'></span> ");
    //child.append(" <br>"); /*or " | "*/
    //child.append("<span onClick='APIflip(this)'>Flip</span>");


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
        if(json.length <= 2 ){
          for(i=0; i < json.length; i++){
            var instance = document.getElementById(json[i].target_instance_id);
            var classList_hold = document.getElementById(json[i].target_instance_id).className.split(/\s+/);
            var concept_id_hold = classList_hold[classList_hold.length-1];
            var master_position_hold = classList_hold[classList_hold.length-2];

            $(instance).removeClass("flipped");
            $(instance).addClass("eng");
            $(instance).removeClass("spa");

            //place concept id on the end of the list
            $(instance).removeClass(master_position_hold);
            $(instance).addClass(master_position_hold);
            $(instance).removeClass(concept_id_hold);
            $(instance).addClass(concept_id_hold);
            

            //fade out, text change, id change
            $(instance).fadeOut('fast');
            $(instance).html('&nbsp;');
            $(instance).append(json[i].origin_instance_text);
            $(instance).attr("id", json[i].origin_instance_id);
            $(instance).fadeIn();
          }

        }//end for if
        //change words
        for(i=0; i < json.length-1; i++){
          var instance = document.getElementById(json[i].target_instance_id);
          var classList_hold = document.getElementById(json[i].target_instance_id).className.split(/\s+/);
          var concept_id_hold = classList_hold[classList_hold.length-1];
          var master_position_hold = classList_hold[classList_hold.length-2];

          $(instance).removeClass("flipped");
          $(instance).addClass("eng");
          $(instance).removeClass("spa");

          //place concept id on the end of the list
          $(instance).removeClass(master_position_hold);
          $(instance).addClass(master_position_hold);
          $(instance).removeClass(concept_id_hold);
          $(instance).addClass(concept_id_hold);
          

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

    var url = "http://diglot.it.et.byu.edu/flip?target_lang=" + target_lang + "&user_id=1&concept_id=" + concept_id;
    console.log(url);
    fetch(url).then((response) => {
        return response.json().then((json) => {
          //console.log("JSON", json);
          if(json.length <= 2 ){
            for(i=0; i < json.length; i++){

            var instance = document.getElementById(json[i].origin_instance_id);
            var classList_hold = document.getElementById(json[i].origin_instance_id).className.split(/\s+/);
            var concept_id_hold = classList_hold[classList_hold.length-1];
            var master_position_hold = classList_hold[classList_hold.length-2];

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
            $(instance).removeClass(master_position_hold);
            $(instance).addClass(master_position_hold);
            $(instance).removeClass(concept_id_hold);
            $(instance).addClass(concept_id_hold);
            

            //fade out, text change, id change
            $(instance).fadeOut('fast');
            $(instance).html('&nbsp;');
            $(instance).append(json[i].target_instance_text);
            $(instance).attr("id", json[i].target_instance_id);
            $(instance).fadeIn();

          }//end for if

          }
          //change words  2 0 1 2 3
          for(i=0; i < json.length-1; i++){

            var instance = document.getElementById(json[i].origin_instance_id);
            var classList_hold = document.getElementById(json[i].origin_instance_id).className.split(/\s+/);
            var concept_id_hold = classList_hold[classList_hold.length-1];
            var master_position_hold = classList_hold[classList_hold.length-2];

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
            $(instance).removeClass(master_position_hold);
            $(instance).addClass(master_position_hold);
            $(instance).removeClass(concept_id_hold);
            $(instance).addClass(concept_id_hold);
            

            //fade out, text change, id change
            $(instance).fadeOut('fast');
            $(instance).html('&nbsp;');
            $(instance).append(json[i].target_instance_text);
            $(instance).attr("id", json[i].target_instance_id);
            $(instance).fadeIn();
          }//end for loop


      });
    });
    //change tags
  }
  else{
    APIflip_back(e);
  }
}
function APIflip_backnew(e){


  //get the instance id
  var span = $(e).parent();
  if(span.hasClass("flipped")){
    span.removeClass("flipped");
    var id = span.attr("id");
    var chunk = span.attr("id");
    var popupChunk = "myPopup" + chunk;
    var word = span.clone().children().remove();
    word = word.end().text().trim();
    var classList = document.getElementById(id).className.split(/\s+/);

    var current_position = sessionStorage.getItem("current_position");
    var target_lang = sessionStorage.getItem("target_lang_id");
    var concept_id = classList[classList.length-1];
    var master_position = classList[classList.length-2];
    var user_id = sessionStorage.getItem("user_id");
    var url = "http://diglot.it.et.byu.edu/flipback?current_pos="+current_position+"&target_lang=" + target_lang + "&user_id="+ user_id+"&concept_id=" + concept_id;
    console.log(url);
    fetch(url).then((response) => {
        return response.json().then((json) => {
          //console.log("JSON", json);
          if(json.length <= 2 ){
            for(i=0; i < json.length; i++){
              var instance = document.getElementById(json[i].target_instance_id);
              var classList_hold = document.getElementById(json[i].target_instance_id).className.split(/\s+/);
              var concept_id_hold = classList_hold[classList_hold.length-1];
              var master_position_hold = classList_hold[classList_hold.length-2];

              $(instance).removeClass("flipped");
              $(instance).addClass("eng");
              $(instance).removeClass("spa");

              //place concept id on the end of the list
              $(instance).removeClass(master_position_hold);
              $(instance).addClass(master_position_hold);
              $(instance).removeClass(concept_id_hold);
              $(instance).addClass(concept_id_hold);
              

              //fade out, text change, id change
              $(instance).fadeOut('fast');
              $(instance).html('&nbsp;');
              $(instance).append(json[i].origin_instance_text);
              $(instance).attr("id", json[i].origin_instance_id);
              $(instance).fadeIn();
            }

          }//end for if
          //change words
          for(i=0; i < json.length; i++){
            var instance = document.getElementById(json[i].target_instance_id);
            //alert(json[i].target_instance_id);
            var classList_hold = document.getElementById(json[i].target_instance_id).className.split(/\s+/);
            var concept_id_hold = classList_hold[classList_hold.length-1];
            var master_position_hold = classList_hold[classList_hold.length-2];

            $(instance).removeClass("flipped");
            $(instance).addClass("eng");
            $(instance).removeClass("spa");

            //place concept id on the end of the list
            $(instance).removeClass(master_position_hold);
            $(instance).addClass(master_position_hold);
            $(instance).removeClass(concept_id_hold);
            $(instance).addClass(concept_id_hold);
            

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
  else{
    span.removeClass("flipped-original");
    var id = span.attr("id");
    var chunk = span.attr("id");
    var popupChunk = "myPopup" + chunk;
    var word = span.clone().children().remove();
    word = word.end().text().trim();
    var classList = document.getElementById(id).className.split(/\s+/);

    var current_position = sessionStorage.getItem("current_position");
    var target_lang = sessionStorage.getItem("target_lang_id");
    var concept_id = classList[classList.length-1];
    var master_position = classList[classList.length-2];
    var user_id = sessionStorage.getItem("user_id");
    var url = "http://diglot.it.et.byu.edu/flipback?current_pos="+current_position+"&target_lang=" + target_lang + "&user_id="+ user_id+"&concept_id=" + concept_id;
    console.log(url);
    fetch(url).then((response) => {
        return response.json().then((json) => {
          //console.log("JSON", json);
          if(json.length <= 2 ){
            for(i=0; i < json.length; i++){
              var instance = document.getElementById(json[i].target_instance_id);
              var classList_hold = document.getElementById(json[i].target_instance_id).className.split(/\s+/);
              var concept_id_hold = classList_hold[classList_hold.length-1];
              var master_position_hold = classList_hold[classList_hold.length-2];

              $(instance).removeClass("flipped");
              $(instance).addClass("eng");
              $(instance).removeClass("spa");

              //place concept id on the end of the list
              $(instance).removeClass(master_position_hold);
              $(instance).addClass(master_position_hold);
              $(instance).removeClass(concept_id_hold);
              $(instance).addClass(concept_id_hold);
              

              //fade out, text change, id change
              $(instance).fadeOut('fast');
              $(instance).html('&nbsp;');
              $(instance).append(json[i].origin_instance_text);
              $(instance).attr("id", json[i].origin_instance_id);
              $(instance).fadeIn();
            }
          }//end for if
          //change words
          for(i=0; i < json.length; i++){
            var instance = document.getElementById(json[i].target_instance_id);
            //alert(json[i].target_instance_id);
            var classList_hold = document.getElementById(json[i].target_instance_id).className.split(/\s+/);
            var concept_id_hold = classList_hold[classList_hold.length-1];
            var master_position_hold = classList_hold[classList_hold.length-2];

            $(instance).removeClass("flipped-original");
            $(instance).addClass("eng");
            $(instance).removeClass("spa");

            //place concept id on the end of the list
            $(instance).removeClass(master_position_hold);
            $(instance).addClass(master_position_hold);
            $(instance).removeClass(concept_id_hold);
            $(instance).addClass(concept_id_hold);
            

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
  
}
function APIflipnew(e){
  //get the instance id

  var span = $(e).parent();
  var text = $(e).parent().text();
  var no_match = text.includes("No target language match");

  if(no_match==false){
    if(span.hasClass("flipped")==false && span.hasClass("flipped-original")==false){
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
      var target_lang = sessionStorage.getItem("target_lang_id");
      var concept_id = classList[classList.length-1];
      var master_position = classList[classList.length-2];
      var current_position = sessionStorage.getItem("current_position");
      var user_id = sessionStorage.getItem("user_id");
      if($(span).hasClass("spa")){
        target_lang = "eng";
      }
      var url = "http://diglot.it.et.byu.edu/flip?current_pos="+current_position+"&target_lang=" + target_lang + "&user_id="+user_id+"&concept_id=" + concept_id;
      console.log(url);
      fetch(url).then((response) => {
          return response.json().then((json) => {
            //console.log("JSON", json);

            if(json.length <= 2 ){
              for(i=0; i < json.length; i++){

                var instance = document.getElementById(json[i].origin_instance_id);
                var classList_hold = document.getElementById(json[i].origin_instance_id).className.split(/\s+/);
                var concept_id_hold = classList_hold[classList_hold.length-1];
                var master_position_hold = classList_hold[classList_hold.length-2];

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
                $(instance).removeClass(master_position_hold);
                $(instance).addClass(master_position_hold);
                $(instance).removeClass(concept_id_hold);
                $(instance).addClass(concept_id_hold);
                

                //fade out, text change, id change
                $(instance).fadeOut('fast');
                $(instance).html('&nbsp;');
                $(instance).append(json[i].target_instance_text);
                $(instance).attr("id", json[i].target_instance_id);
                $(instance).fadeIn();

              }//end for of if

            }
            else{
              //change words  2 0 1 2 3
              for(i=0; i < json.length; i++){

                var instance = document.getElementById(json[i].origin_instance_id);
                //alert(i + " " + json[i].origin_instance_id);
                var classList_hold = document.getElementById(json[i].origin_instance_id).className.split(/\s+/);
                var concept_id_hold = classList_hold[classList_hold.length-1];
                var master_position_hold = classList_hold[classList_hold.length-2];

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
                $(instance).removeClass(master_position_hold);
                $(instance).addClass(master_position_hold);
                $(instance).removeClass(concept_id_hold);
                $(instance).addClass(concept_id_hold);
                

                //fade out, text change, id change
                $(instance).fadeOut('fast');
                $(instance).html('&nbsp;');
                $(instance).append(json[i].target_instance_text);
                $(instance).attr("id", json[i].target_instance_id);
                $(instance).fadeIn();
              }//end for loop
            }



        });
      });
      //change tags
    }
    else{
      APIflip_backnew(e);
    }
  }
}


function APIuser_load(user_id){
  var user_id_local = user_id;
  var url = "http://diglot.it.et.byu.edu/loaduser/" +  user_id;
  console.log(url);
  fetch(url).then((response) => {
      return response.json().then((json) => {
        //console.log("JSON", json);
        sessionStorage.setItem("current_position",json.current_position);
        sessionStorage.setItem("level",json.level);
        sessionStorage.setItem("rate",json.rate);
        sessionStorage.setItem("origin_lang_id",json.origin_lang_id);
        sessionStorage.setItem("target_lang_id",json.target_lang_id);
        sessionStorage.setItem("user_id",json.user_id);
        //window.location.replace("/main");
    });
  });
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
function APIset_preference(){
   var dict = {
    English: "eng",
    Czech: "ces",
    Malay: "msa",
    Spanish: "spa",
    Chinese: "zho",
   };

   var difficulty = document.getElementById("difficulty").value;
   var rate = document.getElementById("rate").value;//need to convert
   var langs = document.getElementsByClassName("active");
   var source_lang = dict[langs[0].textContent];
   var target_lang = dict[langs[1].textContent];
   var uid = sessionStorage.getItem("user_id");
   var url = "http://diglot.it.et.byu.edu/prefs?uid=" + uid + "&origin_lang=" + source_lang + "&target_lang="+ target_lang +"&rate=" + rate + "&level=" + difficulty;
   console.log(url);
   fetch(url).then((response) => {
      return response.json().then((json) => {
        console.log("JSON", json);
        if(json == true){
          $('#settings').modal('toggle');
        }
        else{
          $('.alert').show()
        }
      });
    }); 
}
function logout(){
  sessionStorage.clear();
  window.location.replace("/");
}
function next_chapter(){
  var current_position = sessionStorage.getItem("current_position");
  current_position = current_position.split(":");
  var origin_lang_id = sessionStorage.getItem("origin_lang_id");
  var next_chapter = parseInt(current_position[2]);
  next_chapter++;
  if(next_chapter==2){
    var next_chapter_string = next_chapter.toString();
    if(next_chapter_string.length == 1){
      next_chapter_string = "0" + next_chapter_string;
    }
    var new_current_position = current_position[0] + ":" + current_position[1] +":"+ next_chapter_string;
    sessionStorage.setItem("current_position", new_current_position);

    var uid = sessionStorage.getItem("user_id");

    var url = "http://diglot.it.et.byu.edu/update_position?user_id=" + uid + "&current_pos=" + new_current_position;
     console.log(url);
     fetch(url).then((response) => {
        return response.json().then((json) => {
          console.log("JSON", json);
        });
      }); 

    location.reload();
  }

}
function previous_chapter(){
  var current_position = sessionStorage.getItem("current_position");
  current_position = current_position.split(":");
  var origin_lang_id = sessionStorage.getItem("origin_lang_id");
  var previous_chapter = parseInt(current_position[2]);
  previous_chapter--;
  if(previous_chapter == 1){
    var previous_chapter_string = previous_chapter.toString();
    if(previous_chapter_string.length == 1){
      previous_chapter_string = "0" + previous_chapter_string;
    }
    var new_current_position = current_position[0] + ":" + current_position[1] +":"+ previous_chapter_string;
    sessionStorage.setItem("current_position", new_current_position);
    var uid = sessionStorage.getItem("user_id");

    var url = "http://diglot.it.et.byu.edu/update_position?user_id=" + uid + "&current_pos=" + new_current_position;
     console.log(url);
     fetch(url).then((response) => {
        return response.json().then((json) => {
          console.log("JSON", json);
        });
      }); 

    location.reload();
  }
}
function get_all_flipped(){
  var uid = sessionStorage.getItem("user_id");
  var origin_lang_id = sessionStorage.getItem("origin_lang_id");
  var target_lang_id = sessionStorage.getItem("target_lang_id");
  var url = "http://diglot.it.et.byu.edu/flipped?user_id=" + uid + "&lang=" + origin_lang_id + "&target_lang=" + target_lang_id;
   console.log(url);
   fetch(url).then((response) => {
      return response.json().then((json) => {
        console.log("JSON", json);
      });
    }); 
}
function APIflipnewbackup(e){
  //get the instance id

  var span = $(e).parent();
  var text = $(e).parent().text();
  var no_match = text.includes("No target language match");

  if(no_match==false){
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
      var target_lang = sessionStorage.getItem("target_lang_id");
      var concept_id = classList[classList.length-1];
      var master_position = classList[classList.length-2];
      var current_position = sessionStorage.getItem("current_position");
      var user_id = sessionStorage.getItem("user_id");
      if($(span).hasClass("spa")){
        target_lang = "eng";
      }
      var url = "http://diglot.it.et.byu.edu/flip?current_pos="+current_position+"&target_lang=" + target_lang + "&user_id="+user_id+"&concept_id=" + concept_id;
      console.log(url);
      fetch(url).then((response) => {
          return response.json().then((json) => {
            //console.log("JSON", json);

            if(json.length <= 2 ){
              for(i=0; i < json.length; i++){

                var instance = document.getElementById(json[i].origin_instance_id);
                var classList_hold = document.getElementById(json[i].origin_instance_id).className.split(/\s+/);
                var concept_id_hold = classList_hold[classList_hold.length-1];
                var master_position_hold = classList_hold[classList_hold.length-2];

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
                $(instance).removeClass(master_position_hold);
                $(instance).addClass(master_position_hold);
                $(instance).removeClass(concept_id_hold);
                $(instance).addClass(concept_id_hold);
                

                //fade out, text change, id change
                $(instance).fadeOut('fast');
                $(instance).html('&nbsp;');
                $(instance).append(json[i].target_instance_text);
                $(instance).attr("id", json[i].target_instance_id);
                $(instance).fadeIn();

              }//end for of if

            }
            else{
              //change words  2 0 1 2 3
              for(i=0; i < json.length; i++){

                var instance = document.getElementById(json[i].origin_instance_id);
                //alert(i + " " + json[i].origin_instance_id);
                var classList_hold = document.getElementById(json[i].origin_instance_id).className.split(/\s+/);
                var concept_id_hold = classList_hold[classList_hold.length-1];
                var master_position_hold = classList_hold[classList_hold.length-2];

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
                $(instance).removeClass(master_position_hold);
                $(instance).addClass(master_position_hold);
                $(instance).removeClass(concept_id_hold);
                $(instance).addClass(concept_id_hold);
                

                //fade out, text change, id change
                $(instance).fadeOut('fast');
                $(instance).html('&nbsp;');
                $(instance).append(json[i].target_instance_text);
                $(instance).attr("id", json[i].target_instance_id);
                $(instance).fadeIn();
              }//end for loop
            }



        });
      });
      //change tags
    }
    else{
      APIflip_backnew(e);
    }
  }
}
