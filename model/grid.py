# importation des librairies nécessaires
from PyQt5.QtMultimedia import QSound
from os import walk, path
from random import shuffle


class Grid():
    def __init__(self, view, edit: bool = False):
        self.__level = "grid0.txt"
        self.__nbCaseX = 10
        self.__nbCaseY = 10
        self.__tailleCase = 64
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY // 2, self.__nbCaseX // 2]
        self.__view = view
        self.generateGrid(edit)
        self.__victorySound = QSound('sounds/victorySound.wav')
        self.__defeatSound = QSound('sounds/defeatSound.wav')
        self.__boxDrop = QSound('sounds/boxDrop.wav')
        self.__fallingGuy = QSound('sounds/fallingGuy.wav')

    def getNbCaseX(self):
        return self.__nbCaseX

    def getNbCaseY(self):
        return self.__nbCaseY

    def getTailleCase(self):
        return self.__tailleCase

    def getGrid(self):
        return self.__grid

    def setGrid(self, pos_lig: int, pos_col: int, val_bg: int, val_fg: int):
        self.__grid[0][pos_lig][pos_col] = val_bg
        self.__grid[1][pos_lig][pos_col] = val_fg

    def getPosJoueur(self):
        return self.__posJoueur

    def setLevel(self, file_path: str):
        print(path.relpath(file_path, "grids"))
        self.__level = path.relpath(file_path, "grids")

    def changerLevel(self):
        niveaux = next(walk("grids"))[2]
        for i in range(len(niveaux)):
            if niveaux[i] == self.__level:
                if i + 1 == len(niveaux):
                    self.__level = niveaux[0]
                else:
                    self.__level = niveaux[i + 1]
                break
        self.__grid = []
        self.generateGrid()

    def setPosJoueur(self, pos_ligne: int, pos_colonne: int):
        self.__grid[1][self.__posJoueur[0]][self.__posJoueur[1]] = 0
        self.__grid[1][pos_ligne][pos_colonne] = 2
        self.__posJoueur = [pos_ligne, pos_colonne]

    def deplaceCaisse(self, pos_lig, pos_col, sens) -> bool:
        newPosLig = pos_lig + sens[0]
        newPosCol = pos_col + sens[1]
        # Verifie que la prochaine position de la caisse est dans la grille
        if not (0 <= newPosLig < self.__nbCaseY and 0 <= newPosCol < self.getNbCaseX()):
            return False
        # verifie que ce n'est pas sur un mur, et qu'il n'y a pas déjà une caisse
        elif self.__grid[0][newPosLig][newPosCol] == 1 or self.__grid[1][newPosLig][newPosCol] == 1:
            return False
        # si c'est sur un trou
        elif self.__grid[0][newPosLig][newPosCol] == 2:
            self.__grid[0][newPosLig][newPosCol] = 3
            self.playBoxDropSound()
        # sinon
        else:
            self.__grid[1][newPosLig][newPosCol] = 1
        self.__grid[1][pos_lig][pos_col] = 0
        return True

    def deplacerJoueur(self, sens):
        new_ligne = self.__posJoueur[0] + sens[0]
        new_colonne = self.__posJoueur[1] + sens[1]
        caisse_deplacer = False
        # Verifie que la prochaine position du joueur est dans la grille
        if not (0 <= new_ligne < self.__nbCaseY and 0 <= new_colonne < self.getNbCaseX()):
            return
        # Verifie que ce n'est pas sur un mur
        elif self.__grid[0][new_ligne][new_colonne] == 1:
            return
        # si c'est un trou
        elif self.__grid[0][new_ligne][new_colonne] == 2:
            self.__grid[1][self.__posJoueur[0]][self.__posJoueur[1]] = 0
            self.__view.incrementNbMovement()
            self.__view.updateView()
            self.playDefeatSound()
            self.__view.ecranDeFin("Oh non ! Vous êtes tomber dans un trou et un serpent blanc vous a graille !")
            return
        # Si il y a une caisse
        elif self.__grid[1][new_ligne][new_colonne] == 1:
            if not self.deplaceCaisse(new_ligne, new_colonne, sens):
                return
            caisse_deplacer = True
        self.setPosJoueur(new_ligne, new_colonne)
        self.__view.incrementNbMovement()
        self.__view.updateView()
        if caisse_deplacer and self.isGagner():
            self.playVictorySound()
            self.__view.ecranDeFin("Félicitations ! Vous avez gagné en : " + str(self.__view.getNbOfMovements()) + " mouvements !", True)
        elif caisse_deplacer and self.isPerdu():
            self.playDefeatSound()
            self.__view.ecranDeFin("Dommage, vous avez coincè une caisse !")

    def generateGrid(self, edit: bool = False):
        """
        Valeur pour l'arriere plan (grid[0])
            0 = Sol
            1 = Mur
            2 = Trou
            3 = Trou rebouché
        Valeur pour le premier plan (grid[1])
            0 = Rien
            1 = Caisse
            2 = Joueur
        """
        self.__grid = []
        if edit:
            # initialisation de la grille 3d qui permet de stocker 2 grille 2D,
            # une pour l'arrière plan et une pour le premier plan
            for i in range(2):
                self.__grid.append([])
                for j in range(self.__nbCaseY):
                    self.__grid[i].append([])
                    for k in range(self.__nbCaseX):
                        self.__grid[i][j].append(0)
            return
        # Recuperation de la grille 3D présent dans le fichier du niveau
        with open("grids/" + self.__level, "r") as file:
            line = file.readline()
            k = 0
            i = 0
            self.__grid.append([])
            while line:
                if line == '\n':
                    self.__grid.append([])
                    line = file.readline()
                    k += 1
                    i = 0
                    continue
                self.__grid[k].append([])
                n = ""
                j = 0
                for char in line:
                    if char != " ":
                        n += char
                        continue
                    self.__grid[k][i].append(int(n))
                    if k == 1 and self.__grid[k][i][j] == 2:
                        self.__posJoueur = [i, j]
                    j += 1
                    n = ""
                self.__grid[k][i].append(int(n))
                if k == 1 and self.__grid[k][i][j] == 2:
                    self.__posJoueur = [i, j]
                line = file.readline()
                i += 1

    def regenerateGrid(self):
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY // 2, self.__nbCaseX // 2]
        self.generateGrid()

    def isGagner(self) -> bool:
        for ligne in self.__grid[1]:
            for n in ligne:
                if n == 1:
                    return False
        return True

    def isPerdu(self) -> bool:
        grid = self.__grid
        for i in range(len(grid[0])):
            for j in range(len(grid[0][i])):
                if grid[1][i][j] == 1:
                    for k in [-1, 1]:
                        for l in [-1, 1]:
                            if i + k in [-1, len(grid[0])] and j + l in [-1, len(grid[0][i])]:  # si la caisse est dans un angle de la grille
                                return True
                            elif i + k in [-1, len(grid[0])] and grid[0][i][j + l] == 1:
                                return True
                            elif j + l in [-1, len(grid[0][i])] and grid[0][i + k][j] == 1:
                                return True
                            elif i + k in [-1, len(grid[0])] or j + l in [-1, len(grid[0][i])]:
                                continue
                            elif grid[0][i][j + l] == 1 and grid[0][i + k][j] == 1:
                                return True
        return False

    def playVictorySound(self):
        self.__victorySound.play()

    def playBoxDropSound(self):
        self.__boxDrop.play()

    def playDefeatSound(self):
        self.__defeatSound.play()

    def playFallingGuy(self):
        self.__fallingGuy.play()
