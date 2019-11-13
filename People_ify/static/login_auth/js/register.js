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

    $('#form').submit(function (e) {
        // for csrf token in Ajax
        var csrftoken = Cookies.get('csrftoken'); 
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        // Ajax request
        e.preventDefault();
        console.log("step 1");
        $.ajax({
            type:'POST',
            url:'/register/',
            data:{
                fname:$('#label-fname').val(),
                lname:$('#label-lname').val(),
                uname:$('#label-uname').val(),
                email:$('#label-email').val(),
                passwd:$('#label-password').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddleware]').val()
            },
            success:function(data){
                // alert("Hurray!");
                if (data.message == "no_email") {
                    $('#message').html('<div class="alert alert-danger" role="alert">Error! Looks like email already exists."</div>')
                }
                else if(data.message == "no_uname"){
                    $('#message').html('<div class="alert alert-danger" role="alert">Error! Looks like Username is already taken."</div>');
                }
                else if(data.message=="wrong"){
                    $('#message').html('<div class="alert alert-danger" role="alert">Error! Something went wrong."</div>')
                }
                else if(data.message == "success"){
                    window.location.replace("/album_collection/"+data.userid);
                }
            }
        });
        console.log("form submitted yaar!");
        return false;
    });
});






// form submission

// document.querySelector('#form').onsubmit = () => {

//     const request = new XMLHttpRequest();
//     console.log("form submitted!")
    
//     const fname = document.querySelector('#label-fname').value;
//     const lname = document.querySelector('#label-lname').value;
//     const uname = document.querySelector('#label-dname').value;
//     const email = document.querySelector('#label-email').value;
//     const passwd = document.querySelector('#label-password').value;
   
//     request.open('POST', '/register');
//     request.onload = () => {
//         const data = JSON.parse(request.responseText);
//         if (data.message == "no_mail") {  // check for white-spacing of curly braces
            
//             const contents = '<div class="alert alert-primary" role="alert">Error! Looks like email already exists."</div>';
            
//             document.querySelector('#label-email').value = "";
//             document.querySelector('#label-fname').value = "";
//             document.querySelector('#label-lname').value = "";
//             document.querySelector('#label-uname').value = "";
//             document.querySelector('#label-password').value = "";

//             document.querySelector('#message').innerHTML = contents;

//         } else if (data.message == "no_uname") {
            
//             const contents = '<div class="alert alert-primary" role="alert">Error! Looks like Username is already taken."</div>';

//             document.querySelector('#label-uname').value = "";
//             document.querySelector('#label-password').value = "";
                            
//             document.querySelector('#message').innerHTML = contents;

//         } else if (data.message == "wrong") {
//             const contents = '<div class="alert alert-primary" role="alert">Error! Something went wrong."</div>';

//             document.querySelector('#label-email').value = "";
//             document.querySelector('#label-fname').value = "";
//             document.querySelector('#label-lname').value = "";
//             document.querySelector('#label-uname').value = "";
//             document.querySelector('#label-password').value = "";

//             // window.location.replace("/");
//             document.querySelector('#message').innerHTML = contents;
            
//         }
//     }
//     const data = new FormData();
//     data.append('fname', fname); 
//     data.append('lname', lname);
//     data.append('uname', uname);
//     data.append('email', email);
//     data.append('passwd', passwd);

//     request.send(data);
//     return false;
// }