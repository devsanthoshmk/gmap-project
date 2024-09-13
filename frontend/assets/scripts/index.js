new Vue({
    el: "#app",
    data() {
      return {
        input:"",               //to get the search input from user
        action: "Search",       //to make tha search button dynamic i.e for both download and search
        btncolor: "btn-success", //color of the button to change accordingly
        shaking:"",            //shake search bar to indicate no input value
        spin : true
      }
    },
    methods: {
      //dev meths
      log(ob){
        console.log(ob);
      },
      async act(search){
        let a_lis=[];
        if (search.trim()){ 
            if (this.action==="Search"){
              this.spin=false;
              this.action="";
              this.btncolor='border';
              // await  new Promise(resolve => setTimeout(resolve, 3000));
              fetch(`/download?query=${encodeURIComponent(search)}` )
              .then(response => {
                if (!response.ok) {
                  throw new Error('Network response was not ok');
                }
                return response.blob();
              })
              .then(blob => {
                const url = window.URL.createObjectURL(blob);
                let a = document.createElement('a');
                a.id="del"
                a.href = url;
                a.download = search+'.xlsx'; // Filename for download
                document.body.appendChild(a);
                this.btncolor='btn-primary';
                this.spin=true;
                this.action="Download";
                
              })
              .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
              });
          } else {
            let a= document.getElementById('del');
            a.click();
            a.remove();
            this.btncolor='btn-success'
            this.action="Search";
            this.input="";
          }
             

            
          } 
          
          
        }
      }
    }
  );