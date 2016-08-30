#!/usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room


app = Flask(__name__)
app.config["SECRET_KEY"] = "ggyughlml655khhíjnge55paguitfé'(iij"
chat = True  # active le chat

socket = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    global client_number, li_game, chat
    if request.method == "GET":
        return render_template('connexion.html')
    elif request.method == "POST":
        client_number += 1
        session["number"] = client_number
        pseudo = request.form['pseudo']
        session["pseudo"] = pseudo
        client_number_old = client_number
        if client_number % 2 == 0:
            li_game.append(Game([pseudo, "?"],
                                grille=[['.', '.', '.'] for i in range(3)]))
            joue = 0
        else:
            socket.emit("connecte", broadcast=True)
            joue = 1
            li_game[client_number // 2].pseudos[1] = pseudo
        print("Nouveau joueur numero: {}; pseudo: {}".format(client_number_old,
                                                             pseudo))
        return render_template('morpion.html', joue=joue,
                                client_number=client_number_old, chat=chat,
                                pseudo=pseudo)


###############################################################################
# jeu
###############################################################################


@socket.on('rejoue')
def rejouer():
    client_number = session["number"]
    num_partie = client_number // 2
    print("\npartie num° " + str(num_partie) + " remise a zero")
    #on remet la partie a zero
    li_game[num_partie].grille = [['.', '.', '.'] for i in range(3)]
    li_game[num_partie].commence = 1 - li_game[num_partie].commence
    li_game[num_partie].current_player = li_game[num_partie].commence
    print(li_game[num_partie])
    emit('rejouer', {"gagnant": li_game[num_partie].verif()},
         room=str(num_partie))


@socket.on('connecte')
def connecte():
    """permet de joindre le client a sa partie (room)"""
    client_number = session['number']
    join_room(str(client_number // 2))
    adversaire = li_game[client_number // 2].pseudos[1 - (client_number % 2)]
    print("\n\ndgfgfnlkfg : " + str(li_game[client_number // 2].pseudos))
    socket.emit("nom_adversaire",
                {"nom_adversaire": li_game[client_number // 2].pseudos},
                room=str(client_number // 2))
    return {"adv_present": abs(li_game[client_number // 2].commence
                          - (client_number % 2)),
            "nom_adversaire": adversaire}


@socket.on("joue")
def joue(msg):
    """appeller lorsqu'un joueur a joue"""
    x = msg['x']
    y = msg['y']
    joueur = session["number"]
    print("tentative de jouer de " + str(joueur))
    if joueur % 2 == li_game[joueur // 2].current_player:
        print("{} a jouer en {},{}".format(joueur, x, y))
        if li_game[joueur // 2].jouer(x, y) is None:
            emit("jouer", {'x': x, 'y': y, "pers": ["X", "O"][joueur % 2]},
                 room=str(joueur // 2))
            ver = li_game[joueur // 2].verif()
            if ver != '.':
                if ver == "N":
                    emit("gagne", {"pers": "N"},
                         room=str(joueur // 2))
                else:
                    li_game[joueur // 2].score[joueur % 2] += 1
                    emit("gagne", {"pers": ["X", "O"][joueur % 2],
                         "score": li_game[joueur // 2].score[joueur % 2]},
                         room=str(joueur // 2))

###############################################################################
# chat
###############################################################################


if chat:
    @socket.on('envoi')
    def envoi(msg):
        msg = msg["msg"]
        joueur = session["number"]
        partie = str(joueur // 2)
        emit('recoi', {"msg": msg, "pers": ["X", "O"][joueur % 2],
             'pseudo': session['pseudo']}, room=partie)


@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(400)
def error(e):
    return render_template('error.html', error=e)


if __name__ == '__main__':
    client_number = -1
    li_game = []  # liste des parties
    socket.run(app, host="192.168.1.14", port=42629, debug=True)