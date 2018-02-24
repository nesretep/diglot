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
         //console.log(this.verses);
         

      })
    })
  },
  updated: function() {
    $("span:contains(()").html('&nbsp;(');
    var text = $("span:contains(()").next().text().trim();
    //alert(text);
    $("span:contains(()").next().text(text);
  }
})

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
