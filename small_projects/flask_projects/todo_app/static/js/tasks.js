String.prototype.format = function() {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k]);
    }
    return a;
}

var socket;
$(document).ready(function() {
    socket = io.connect('/');

    socket.on('new_task_response', function(msg) {
        const success = msg['success'];
        if (success) {
            location.reload();
        } else {
            alert("Invalid input. Your post has to contain more than spaces.");
        }
    })

    socket.on('reload_page', function() {
        location.reload();
    })

    $("#post-button").click(function() {
        const content = $("#task-content").val();
        socket.emit('new_task', {
            content: content
        })
    })
})

function delete_task(id) {
    socket.emit('delete_task', {
        id: id
    })
}