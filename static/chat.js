var socket = io.connect('http://' + document.domain + ':' + location.port);

var entree = document.getElementById("entree");

var cadre = document.getElementById("discussion");

var divi_old;

function ecrit(text, pers){
    var mess = document.createElement('p');
    var divi = document.createElement("div");
    var messText = document.createTextNode(text);
    mess.appendChild(messText);
    divi.id = "ligne";
    if (pers=="X"){
        mess.id = "mess_X";
        divi.style.right = "5px";
    }
    else{
        mess.id = "mess_O";
        divi.style.left = "5px";
    }

    divi.appendChild(mess);
    cadre.insertBefore(divi, divi_old);
    divi_old = divi;
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



