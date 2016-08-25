#!/usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, join_room, rooms


app = Flask(__name__)
app.config["SECRET_KEY"] = "ggyughlml655khhíjnge55paguitfé'(iij"
chat = False  # active le chat

socket = SocketIO(app)


@app.route('/')
def index():
    global client_number, li_game, chat
    client_number += 1
    session["number"] = client_number
    client_number_old = client_number
    if client_number % 2 == 0:
        li_game.append(Game(grille=[['.', '.', '.'] for i in range(3)]))
        joue = 0
    else:
        socket.emit("connecte", broadcast=True)
        joue = 1
    print("Nouveau joueur numero: {}".format(client_number_old))
    return render_template('morpion.html', joue=joue,
                            client_number=client_number_old, chat=chat)


###############################################################################
# jeu
###############################################################################

@socket.on('connecte')
def connecte():
    """permet de joindre le client a sa partie (room)"""
    session["number"] = client_number
    join_room(str(client_number // 2))


@socket.on("joue")
def joue(msg):
    """appeller lorsqu'un joueur a joue"""
    x = msg['x']
    y = msg['y']
    joueur = session["number"]
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
                    emit("gagne", {"pers": ["X", "O"][joueur % 2]},
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
        emit('recoi', {"msg": msg, "pers": ["X", "O"][joueur % 2]}, room=partie)


if __name__ == '__main__':
    client_number = -1
    li_game = []  # liste des parties
    socket.run(app, host="192.168.1.14", port=42629, debug=True)