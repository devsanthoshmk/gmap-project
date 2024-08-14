new Vue({
    el: "#app",
    data() {
      return {
        input:"",               //to get the search input from user
        action: "Search",       //to make tha search button dynamic i.e for both download and search
        btncolor: "btn-success", //color of the button to change accordingly
        wrong:false
      }
    },
    methods: {
      //dev meths
      log(ob){
        console.log(ob);
      },
      act(search){
        if (search.trim()){  
          if (this.action==="Search"){
            this.action="Download";
            this.btncolor='btn-primary'
          } else {
            this.btncolor='btn-success'
            this.action="Search";
          }
        } else{
          this.wrong=true
        }
      }
    },
    created() {
    }
  });