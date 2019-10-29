document.addEventListener('DOMContentLoaded', () => {
    var isopen = false;
    document.querySelector('.openbtn').onclick = () => {
        if(isopen==false){
            document.getElementById("mySidebar").style.width = "250px";
            document.getElementById("main").style.marginLeft = "250px";
            isopen = true;
        }
        
    }
      
   document.querySelector('.closebtn').onclick = () => {
        if(isopen==true){
            isopen = false;  
            document.getElementById("mySidebar").style.width = "0px";
            document.getElementById("main").style.marginLeft= "0px";
        }
    }
});
