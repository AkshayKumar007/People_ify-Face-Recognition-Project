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
    document.querySelector('#form').onsubmit = () => {

        const request = new XMLHttpRequest();

        const fname = document.querySelector('#fname').value;
        const dname = document.querySelector('#dname').value;
        const email = document.querySelector('#email').value;
        const passwd = document.querySelector('#passwd').value;
       
        request.open('POST', '/register');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.message == "no_mail") {// check for white-spacing of curly braces
                
                const contents = '<div class="alert alert-primary" role="alert">Error! Looks like email already exists."</div>';
                
                document.querySelector('#fname').value = "";
                document.querySelector('#dname').value = "";
                document.querySelector('#email').value = "";
                document.querySelector('#passwd').value = "";

                document.querySelector('#message').innerHTML = contents;

            } else if (data.message == "no_uname") {
                
                const contents = '<div class="alert alert-primary" role="alert">Error! Looks like DName is already taken."</div>';

                document.querySelector('#dname').value = "";
                document.querySelector('#passwd').value = "";
                                
                document.querySelector('#message').innerHTML = contents;

            } 
            // else if (data.message == "success") {
            //     document.querySelector('#fname').value = "";
            //     document.querySelector('#dname').value = "";
            //     document.querySelector('#email').value = "";
            //     document.querySelector('#passwd').value = "";
            //     // request.open('GET', '/channel_list');// may break code
            //     window.location.replace("/");
                
            // }
        }
        const data = new FormData();
        data.append('fname', fname); 
        data.append('dname', dname);
        data.append('email', email);
        data.append('passwd', passwd);
    
        request.send(data);
        return false;
    }
});