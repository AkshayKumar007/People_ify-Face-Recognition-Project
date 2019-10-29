document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.openbtn').onclick = () => {
        document.getElementById("mySidebar").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
    }
      
   document.querySelector('.closebtn').onclick = () => {
        document.getElementById("mySidebar").style.width = "0px";
        document.getElementById("main").style.marginLeft= "0px";
    }
});
