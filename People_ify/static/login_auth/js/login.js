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
            url:'/login/',
            data:{
                uname:$('#label-uname').val(),
                passwd:$('#label-password').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddleware]').val()
            },
            success:function(data){
                // alert("Hurray!");
                if (data.message == "iep") {
                    $('#message').html('<div class="alert alert-danger" role="alert">Invalid email or password!"</div>')
                }
                else if(data.message == "success"){
                    alert("inside!");
                    var x = "/album-collection/" + data.userid;
                    $.get(x);
                }
            }
        });
        console.log("form submitted yaar!");
        return false;
    });
});