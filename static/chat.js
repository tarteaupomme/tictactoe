var socket = io.connect('http://' + document.domain + ':' + location.port);

var entree = document.getElementById("entree");

var textarea = document.getElementById("discussion");

function ecrit(text, pers){
    textarea.value  = pers + " dit : " + text + "\n" + textarea.value;
}






function envoi(event){
    if (event.keyCode == 13){
        msg = event.target.value;
        event.target.value ="";
        socket.emit('envoi', {msg: msg});
    }
}



socket.on('recoi', function(data){
    msg = data.msg;
    pers = data.pers;
    ecrit(msg, pers);
});



