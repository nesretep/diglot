new Vue({
  el: '#chapter',
  data: () => ({
    json: {},
    verses: []
  }),
  created: function() {
    fetch('http://diglot.it.et.byu.edu/eng/1Nephi/01').then((response) => {
      return response.json().then((json) => {
        //console.log("JSON", json)
        this.json = json
        
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
         console.log(this.verses);
         

      })
    })
  }
})
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

function popupVue() {

       var alreadyPopup = document.getElementsByClassName("popuptext");
       var exists = $(event.target).children().attr("id");
       var chunk = $(event.target).attr("id");
       //checks if there is already a pop up
       //if there is, delete it
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
              child.append("<span onclick='flip_the_phrase3(this);'>Flip</span>");
              child.append(" | ");
              child.append(" <span onclick='define(this)'>Define</span> ");


              var popupChunk = "myPopup" + chunk;
              var popup = document.getElementById(popupChunk);
              popup.classList.toggle("show");
       }
       else{
              var span = $(event.target);
              span.children().remove();
       }
}
/*Test JSON pull
var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://diglot.it.et.byu.edu/eng/1Nephi/01",
  "method": "GET",
  "headers": {
    "accept": "application/json",
    "content-type": "application/json",
    "cache-control": "no-cache",
    "postman-token": "358adb71-556a-a6c9-046b-c2dda6336398"
  }
}

$.ajax(settings).done(function (response) {
  console.log(response);
});
*/

/*
var xmlHttp = new XMLHttpRequest();
xmlHttp.onreadystatechange = function() { 
 if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
     callback(xmlHttp.responseText);
}
xmlHttp.open("GET", "http://diglot.it.et.byu.edu/eng/1Nephi/01", true); // true for asynchronous 
xmlHttp.send(null);
alert(xmlHttp.responseText);
document.getElementById("demo").innerHTML = xmlHttp.responseText;
*/