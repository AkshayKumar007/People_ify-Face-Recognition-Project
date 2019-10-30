document.addEventListener('DOMContentLoaded', () => {
    var isopen = false;

    document.querySelector('.closebtn').onclick = () => {
        if(isopen==false){
            document.getElementById("mySidebar").style.width = "450px";
            isopen = true;
        }
        else if(isopen==true){
            isopen = false;  
            document.getElementById("mySidebar").style.width = "63px";            
        }
    }

    // const a = document.querySelectorAll('.img1');
    // a.style.animationPlayState() = 'paused';
    window.onscroll = () => {
        console.log('----');
        console.log(window.innerHeight);
        console.log(window.scrollY);
        console.log(document.body.offsetHeight);
        if (window.scrollY >= window.innerHeight) {
            // a.style.animationDirection =  "reverse";
            document.querySelector('body').style.background = 'green';

        } else {
            // a.style.animationDirection =  "normal";
            document.querySelector('body').style.background = 'white';
        }
    };
  
  
});

