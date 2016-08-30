# -*- coding: utf-8 -*-


class Game:
    def __init__(self, grille=[['.', '.', '.'] for i in range(3)],
                                                current_player=0):
        self.grille = grille
        self.current_player = current_player
        self.dernier_coup = None
        self.commence = 0

    def verif(self):
        for line in self.grille:  # en ligne
            if line == ['X', 'X', 'X']:
                return "X"
            if line == ['O', 'O', 'O']:
                return "O"

        for i in range(3):  # en colone
            col = [self.grille[j][i] for j in range(3)]
            if col == ['X', 'X', 'X']:
                return "X"
            if col == ['O', 'O', 'O']:
                return "O"

        dia = [self.grille[i][i] for i in range(3)]  # diagonnale 1
        if dia == ['X', 'X', 'X']:
            return "X"
        if dia == ['O', 'O', 'O']:
            return "O"

        dia = [self.grille[i][2 - i] for i in range(3)]  # diagonnale 2
        if dia == ['X', 'X', 'X']:
            return "X"
        if dia == ['O', 'O', 'O']:
            return "O"

        li = []  # match nul
        [li.extend(i) for i in self.grille]
        if not "." in li:
            return "N"

        return "."

    def jouer(self, x, y):
        if self.grille[int(x)][int(y)] == ".":
            self.grille[int(x)][int(y)] = ['X', 'O'][self.current_player]
            self.current_player = (self.current_player + 1) % 2
            self.dernier_coup = x, y
            return
        else:
            return "impossible"

    def __str__(self):
        ch = ""
        for i in self.grille:
            ch += str(i) + "\n"
        ch += "current_player: " + ["X", "O"][self.current_player] + "\n"
        return ch

    def __repr__(self):
        return self.__str__()
