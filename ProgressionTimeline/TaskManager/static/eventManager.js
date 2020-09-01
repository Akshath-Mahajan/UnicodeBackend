function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
csrf=getCookie('csrftoken')
function ToggleCompletion(e) {
    id = e.target.parentNode.parentNode.id;
    $.ajax({
        url: "/task/toggle-complete/",
        method: "POST",
        data:{'task_id':id, 'csrfmiddlewaretoken':csrf},
        success: function(data, code, xhr){
            if(xhr.responseText === "True"){
                //Task is now complete
                e.target.textContent = 'Mark Incomplete'
                $('#complete-tasks-list').prepend($('#'+id))
            }
            if(xhr.responseText === "False"){
                //Task is now incomplete
                e.target.textContent = 'Mark Complete'
                $('#incomplete-tasks-list').prepend($('#'+id))
            }
            if(xhr.responseText === "No pls"){
                alert("You can't do that! Please refresh your page")
            }
        }
    });
}
$(document).ready(() => $(".toggle-btn").click((e)=>ToggleCompletion(e)))


