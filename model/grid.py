# importation des librairies nécessaires
from PyQt5.QtMultimedia import QSound

class Grid():
    def __init__(self):
        self.__nbCaseX = 10
        self.__nbCaseY = 10
        self.__tailleCase = 64
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY//2, self.__nbCaseX//2]
        self.__view = None
        self.generateGrid()
        self.__victorySound = QSound('sounds/victorySound.wav')
        self.__defeatSound = QSound('sounds/defeatSound.wav')
        self.__boxDrop = QSound('sounds/boxDrop.wav')

    def setView(self, view):
        self.__view = view

    def getNbCaseX(self):
        return self.__nbCaseX

    def getNbCaseY(self):
        return self.__nbCaseY

    def getTailleCase(self):
        return self.__tailleCase

    def getGrid(self):
        return self.__grid

    def getPosJoueur(self):
        return self.__posJoueur

    def setPosJoueur(self, pos_ligne: int, pos_colonne: int):
        self.__grid[self.__posJoueur[0]][self.__posJoueur[1]] = 0
        self.__grid[pos_ligne][pos_colonne] = 4
        self.__posJoueur = [pos_ligne, pos_colonne]

    def deplaceCaisse(self, pos_lig, pos_col, sens) -> bool:
        newPosLig = pos_lig + sens[0]
        newPosCol = pos_col + sens[1]
        # Verifie que la prochaine position de la caisse est dans la grille
        if not (0 <= newPosLig < self.__nbCaseY and 0 <= newPosCol < self.getNbCaseX()):
            return False
        # verifie que ce n'est pas un mur, ni une autre caisse, ni une caisse sur un trou rebouché
        elif self.__grid[newPosLig][newPosCol] in [1, 2, 7]:
            return False
        # si c'est un trou
        elif self.__grid[newPosLig][newPosCol] == 3:
            self.__grid[newPosLig][newPosCol] = 5
            self.playBoxDropSound()
        # si c'est un trou rebouché
        elif self.__grid[newPosLig][newPosCol] == 5:
            self.__grid[newPosLig][newPosCol] = 7
            self.playBoxDropSound()
        # sinon
        else:
            self.__grid[newPosLig][newPosCol] = 2
        self.__grid[pos_lig][pos_col] = 0
        return True

    def deplacerJoueur(self, sens):
        new_ligne = self.__posJoueur[0]+sens[0]
        new_colonne = self.__posJoueur[1]+sens[1]
        # Verifie que la prochaine position du joueur est dans la grille
        if not (0 <= new_ligne < self.__nbCaseY and 0 <= new_colonne < self.getNbCaseX()):
            return
        # Verifie que ce n'est pas un mur ou un trou
        elif self.__grid[new_ligne][new_colonne] in [1, 3]:
            return
        # Si il y a une caisse
        elif self.__grid[new_ligne][new_colonne] == 2:
            if not self.deplaceCaisse(new_ligne, new_colonne, sens):
                return
            # si le joueur est sur un trou rebouché
            if self.__grid[new_ligne - sens[0]][new_colonne - sens[1]] == 6:
                self.setPosJoueur(new_ligne, new_colonne)
                self.__grid[new_ligne - sens[0]][new_colonne - sens[1]] = 5
            else:
                self.setPosJoueur(new_ligne, new_colonne)
        # si c'est une caisse sur un trou
        elif self.__grid[new_ligne][new_colonne] == 7:
            if not self.deplaceCaisse(new_ligne, new_colonne, sens):
                return
            self.setPosJoueur(new_ligne, new_colonne)
            self.__grid[new_ligne][new_colonne] = 6
        # si c'est un trou rebouché
        elif self.__grid[new_ligne][new_colonne] == 5:
            self.setPosJoueur(new_ligne, new_colonne)
            self.__grid[new_ligne][new_colonne] = 6
        # si le joueur est sur un trou rebouché
        if self.__grid[new_ligne-sens[0]][new_colonne-sens[1]] == 6:
            self.setPosJoueur(new_ligne, new_colonne)
            self.__grid[new_ligne - sens[0]][new_colonne - sens[1]] = 5
        # si c'est une case vide
        if self.__grid[new_ligne][new_colonne] == 0:
            self.setPosJoueur(new_ligne, new_colonne)
        self.__view.incrementNbMovement()
        self.__view.updateView()
        if self.isGagner():
            self.__view.ecranVictoire()


    def generateGrid(self):
        with open("grids/grid0.txt", "r") as file:
            line = file.readline()
            i = 0
            while line:
                self.__grid.append([])
                n = ""
                j = 0
                for char in line:
                    if char != " ":
                        n += char
                        continue
                    self.__grid[i].append(int(n))
                    if int(n) == 4:
                        self.__posJoueur = [i, j]
                    j += 1
                    n = ""
                self.__grid[i].append(int(n))
                line = file.readline()
                i += 1

    def regenerateGrid(self):
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY//2, self.__nbCaseX//2]
        self.generateGrid()

    def isGagner(self) -> bool:
        for ligne in self.__grid:
            for n in ligne:
                if n == 3:
                    return False
        return True

    def playVictorySound(self):
        self.__victorySound.play()

    def playBoxDropSound(self):
        self.__boxDrop.play()

    def playDefeatSound(self):
        self.__defeatSound.play()




