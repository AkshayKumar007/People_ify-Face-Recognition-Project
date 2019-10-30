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

    window.onscroll = () => {
        console.log('----');
        console.log(window.innerHeight);
        console.log(window.scrollY);
        console.log(document.body.offsetHeight);

        if (window.scrollY + window.innerHeight >= 2 * window.innerHeight) {
            document.querySelectorAll('.target1').forEach(current_ele => {
                current_ele.classList.remove('img1');                              
            });
            document.querySelectorAll('.target2').forEach(current_ele => {
                current_ele.classList.remove('img2');                              
            });
            document.querySelectorAll('.target3').forEach(current_ele => {
                current_ele.classList.remove('img3');                              
            });
            document.querySelector('body').style.background = 'green';  
        } else {
            document.querySelectorAll('.target1').forEach(current_ele => {
                current_ele.classList.add('img1');
            });   
            document.querySelectorAll('.target2').forEach(current_ele => {
                current_ele.classList.add('img2');
            });         
            document.querySelectorAll('.target3').forEach(current_ele => {
                current_ele.classList.add('img3');
            });  
            document.querySelector('body').style.background = 'white';
        }
        
    };
    
});


