var current_position = sessionStorage.getItem("current_position");
current_position = current_position.split(":");
var origin_lang_id = sessionStorage.getItem("origin_lang_id");

new Vue({
  el: '#chapter',
  data: () => ({
    json: {},
    verses: [],
    chapter: ""
  }),
  created: function() {
    
    var url = 'http://diglot.it.et.byu.edu/'+ origin_lang_id +'/' + current_position[1] +'/'+ current_position[2];
    console.log(url);
    fetch(url).then((response) => {
      return response.json().then((json) => {
        console.log("JSON", json)
        this.json = json
        this.json.chapter = current_position[2];
        //mark punctuation
        for (i = 0; i < this.json.length; i++) {
              var position = this.json[i].master_position;
              position = position.split(":");
              if(position[0]=="00" && position[1]=="00"){
                     this.json[i].punctuation = true;
              }
              else{
                     this.json[i].punctuation = false;
              }
        }
        //console.log("JSON", this.json);
        
        //get total verses
        for (i = 0; i < this.json.length; i++) {
          var position = this.json[i].instance_id;
          var res = position.split(":");
          var verse = res[3];
          verse = parseInt(verse, 10);
          //alert(verse);
          //empty array
          if(this.verses.length == 0){
              this.verses.push(verse);
          }
          //if the last one matches
          else if(this.verses[this.verses.length-1]== verse){
              //do nothing
              //alert(verses[verses.length-1] + " v:" + verse);
          }
          //if the last one doesn't match
          else{
              this.verses.push(verse);
          }
          //append to each chunk object
          this.json[i].verse = verse;
         }
         //console.log(this.verses);
         

      })
    })
  },
  updated: function() {
    //clean up punctuation
    /*$("span:contains(()").html('&nbsp;(');
    var text = $("span:contains(()").next().text().trim();
    $("span:contains(()").next().text(text);
    */ 
    var punctuation_spans = document.getElementsByClassName("punctuation");

    var punctuation = punctuation_spans[0].textContent;
    var clean_punctuation = punctuation.trim();
    var previous_text = $(punctuation_spans[0]).parent().prev().children().text();
    var new_string = previous_text.trim() + clean_punctuation;
    $(punctuation_spans[0]).parent().prev().children().text(new_string);
    //alert(previous_span);
    punctuation_spans[0].remove();
    /*
    while(punctuation_spans.length > 0){

    }*/ 

    var uid = sessionStorage.getItem("user_id");
    var origin_lang_id = sessionStorage.getItem("origin_lang_id");
    var target_lang_id = sessionStorage.getItem("target_lang_id");
    var current_position = sessionStorage.getItem("current_position");
    var url = "http://diglot.it.et.byu.edu/flipped?current_pos="+current_position+"&user_id=" + uid + "&lang=" + origin_lang_id + "&target_lang=" + target_lang_id;
    console.log(url);
    fetch(url).then((response) => {
      return response.json().then((json) => {
        console.log("JSON", json);
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


  }
})
