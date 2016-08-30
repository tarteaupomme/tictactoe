var elem = document.getElementById('myCanvas');
var context = elem.getContext('2d');

var socket = io.connect('http://' + document.domain + ':' + location.port);

var adv_present;

var moi = parseInt(document.getElementById("joue").getAttribute("joue"));

var score = {moi: 0, adv: 0};

var score_moi = document.getElementById("score_moi");
var score_adv = document.getElementById("score_adv");

var nom_adv = document.getElementById("nom_adv");


var chargement = document.getElementById("chargement");

var pseudo = document.getElementById("pseudo").getAttribute('pseudo');

function grille(context, taille_x, taille_y){
    context.srokeStyle = '#000000';
    context.strokeRect(0, 0, parseInt(taille_x / 3), taille_y);
    context.strokeRect(0, 0, parseInt((2 / 3)* taille_x), taille_y);
    context.strokeRect(0, 0, taille_x, taille_y);
    context.strokeRect(0, parseInt(taille_y / 3), taille_x, parseInt(taille_y / 3));
}

function init(){
    grille(context, elem.width, elem.height);
    socket.on('nom_adversaire', function(data){
        nom_adv.innerHTML = data.nom_adversaire[1 - moi];
    });
    socket.emit('connecte', function(data){
        adv_present = data.adv_present;
        if (adv_present){
            elem.style.cursor = "progress";
            chargement.innerHTML = "L'adversaire joue, veuillez patienter";
            jouer();
        }
        else{
            elem.style.cursor = "crosshair";
            chargement.innerHTML = "A vous de jouer";
            jouer();
        }
    });
}

function trouve_coor(x, y){
        return [parseInt(x/200),parseInt(y/200)];
}

function affiche(context, taille_x, taille_y, x, y, pers){
    context.lineWidth = 4;
    if (pers=="X"){
        context.strokeStyle = '#FF0000';
        context.beginPath();
        context.lineCap = 'round';

        context.moveTo(x * taille_x / 3 + 20, y * taille_y/3 + 20);
        context.lineTo((x + 1) * taille_x / 3 - 20, (y + 1) * taille_y/3 - 20);

        context.moveTo(x * taille_x / 3 + 20, (y +1) * taille_y/3 - 20);
        context.lineTo((x + 1) * taille_x / 3 - 20, y * taille_y/3 + 20);
        context.stroke();
    }
    else if (pers == "O"){
        context.strokeStyle = '#0900FF';
        context.beginPath();
        context.arc((taille_x / 6) + (taille_x / 3) * x,
             (taille_y / 6) + (taille_y / 3) * y,
             (taille_x / 6) - 20, 0, Math.PI * 2);
        context.stroke();
    }
    context.lineWidth = 1;
    context.strokeStyle = "#000000";
}

function clear(context, elem){
    context.clearRect(0, 0, elem.width, elem.height);
}

function clique(event){
    var x = event.clientX - elem.offsetLeft;
    var y = event.clientY - elem.offsetTop;
    coor = trouve_coor(x, y);
    x = coor[0];
    y = coor[1];
    chargement.innerHTML = "Envoie au serveur, veuillez patienter...";
    socket.emit("joue", {x: x, y: y});
}

function jouer(){
    chargement.innerHTML = "adversaire conecté";
    socket.on("jouer", function(msg){
        var x = parseInt(msg.x);
        var y = parseInt(msg.y);
        var pers = msg.pers;
        affiche(context, elem.width, elem.height, x, y, pers);
        if (pers == ["X", "O"][moi]){
            elem.style.cursor = "progress";
            chargement.innerHTML = "L'adversaire joue, veuillez patienter";
        }
        else{
            elem.style.cursor = "crosshair";
            chargement.innerHTML = "A vous de jouer";
        }
    });


    socket.on('gagne', function(msg){
        if (msg.pers == "N"){
            chargement.innerHTML = "Match nul !!";
        }
        else{
            chargement.innerHTML = msg.pers + " a gagné";
            if (msg.pers == ["X", "O"][moi]){
                score.moi = msg.score;
            }
            else{
                score.adv = msg.score;
            }
            score_moi.innerHTML = score.moi;
            score_adv.innerHTML = score.adv;
        }
        elem.removeEventListener('click', clique);
    });

    elem.addEventListener('click', clique);

    socket.on('rejouer', rejouer);
}

function rejouer(data){
    var gagnant = data.gagnant;
    clear(context, elem);
    init();
    elem.style.cursor = adv_present ? "crosshair" : "progress";

}

function veut_rejouer(){
    socket.emit('rejoue');
}


init();


