var socket = io.connect('http://' + document.domain + ':' + location.port);

var entree = document.getElementById("entree");

var cadre = document.getElementById("chat");


function ecrit(text, pers){
    var mess = document.createElement('p');
    if (pers=="X"){
        mess.style.textAlign = "right";
    }
    else{
        mess.style.textAlign = "left";
    }
    cadre.appendChild(mess);
    var messText = document.createTextNode(text);
    mess.appendChild(messText);
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



