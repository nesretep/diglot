var current_position = sessionStorage.getItem("current_position");
current_position = current_position.split(":");
var origin_lang_id = sessionStorage.getItem("origin_lang_id");

new Vue({
  el: '#chapter',
  data: () => ({
    json: {},
    verses: []
  }),
  created: function() {
    var url = 'http://diglot.it.et.byu.edu/'+ origin_lang_id +'/' + current_position[1] +'/'+ current_position[2];
    console.log(url);
    fetch(url).then((response) => {
      return response.json().then((json) => {
        console.log("JSON", json)
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
    //clean up punctuation
    /*$("span:contains(()").html('&nbsp;(');
    var text = $("span:contains(()").next().text().trim();
    $("span:contains(()").next().text(text);
    */  
  }
})
