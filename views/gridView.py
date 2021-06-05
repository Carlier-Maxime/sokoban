# importation des librairies utiles
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QLabel, QPushButton, QGridLayout, QWidget, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt
from controllers.crtlMouvement import CrtlMouvement
from model.grid import Grid


class GridView(QMainWindow):
    def __init__(self, model: Grid, controller: CrtlMouvement):
        super(GridView, self).__init__()
        self.__model = model
        self.__controller = controller
        self.setFixedSize(self.__model.getNbCaseX() * self.__model.getTailleCase(),
                          self.__model.getNbCaseY() * self.__model.getTailleCase())
        # menu
        self.__menuBar = self.menuBar()
        self.__menuJeu = self.__menuBar.addMenu("Jeu")
        self.__menuHelp = self.__menuBar.addMenu("Aide")

        self.__restartAction = QAction("Rejouer", self)
        self.__quitAction = QAction("Quitter", self)
        self.__helpAction = QAction("Afficher l'aide", self)

        self.__helpAction.triggered.connect(self.helpView)  # A modifier pour expliquer le but du jeu
        self.__quitAction.triggered.connect(quit)
        self.__restartAction.triggered.connect(self.restart)

        self.__menuJeu.addAction(self.__restartAction)
        self.__menuJeu.addAction(self.__quitAction)
        self.__menuHelp.addAction(self.__helpAction)

        # bottom statut bar
        self.__statutBar = self.statusBar()
        self.__nbOfMovements = 0
        self.__labelNbMove = QLabel()
        self.__labelNbMove.setText("Nombre de Mouvements : "+str(self.__nbOfMovements))
        self.__labelStatut = QLabel()
        self.__labelStatut.setText("")
        self.__statutBar.addPermanentWidget(self.__labelNbMove, 1)
        self.__statutBar.addPermanentWidget(self.__labelStatut, 2)


        # controller / central widget + GridLayout
        self.__GridLayout = QGridLayout(self.__controller)
        self.__controller.setLayout(self.__GridLayout)
        self.setCentralWidget(self.__controller)
        self.__controller.setFocus()

        self.updateView()

    def getModel(self):
        return self.__model

    def getController(self):
        return self.__controller

    def incrementNbMovement(self):
        self.__nbOfMovements += 1

    def updateView(self):
        # suppresion de tous les widget enfant de GridLAyout (layout.removeAllWidget())
        for i in reversed(range(self.__GridLayout.count())):
            widget_to_remove = self.__GridLayout.itemAt(i).widget()
            # remove it from the layout list
            self.__GridLayout.removeWidget(widget_to_remove)
            # remove it from the gui
            widget_to_remove.setParent(None)
        # remplissage de la grille
        grid = self.__model.getGrid()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                case = QWidget()
                case.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                if grid[i][j] == 0:  # case vide
                    case.setStyleSheet("background-image: url(images/SOL.png);")
                elif grid[i][j] == 1:  # mur
                    case.setStyleSheet("background-image: url(images/MUR.png);")
                elif grid[i][j] == 2:  # caisse
                    case.setStyleSheet("background-image: url(images/BOX.png);")
                elif grid[i][j] == 3:  # trou
                    case.setStyleSheet("background-image: url(images/TROU.png);")
                elif grid[i][j] == 4:  # joueur
                    case2 = QWidget()
                    case2.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                    case2.setStyleSheet("background-image: url(images/SOL.png);")
                    self.__GridLayout.addWidget(case2, i, j)
                    case.setStyleSheet("background-image: url(images/Perso.png);")
                elif grid[i][j] == 5:  # trou bouché
                    case.setStyleSheet("background-image: url(images/TROU_BOUCHER.png);")
                elif grid[i][j] == 6:  # trou boucher + joueur
                    case2 = QWidget()
                    case2.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                    case2.setStyleSheet("background-image: url(images/TROU_BOUCHER.png);")
                    self.__GridLayout.addWidget(case2, i, j)
                    case.setStyleSheet("background-image: url(images/Perso.png);")
                elif grid[i][j] == 7:  # trou boucher + caisse
                    case2 = QWidget()
                    case2.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                    case2.setStyleSheet("background-image: url(images/TROU_BOUCHER.png);")
                    self.__GridLayout.addWidget(case2, i, j)
                    case.setStyleSheet("background-image: url(images/BOX.png);")
                self.__GridLayout.addWidget(case, i, j)
        # update nb movements
        self.__labelNbMove.setText("Nombre de Mouvements : "+str(self.__nbOfMovements))

    def ecranVictoire(self):
        self.setFocus()
        self.__labelStatut.setText("YOU WIN !!!")

    def restart(self):
        self.__labelStatut.setText("")
        self.setCentralWidget(self.__controller)
        self.__model.regenerateGrid()
        self.__nbOfMovements = 0
        self.updateView()
        self.__controller.setFocus()

    def helpView(self):
        dialog = QDialog()
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowTitle("Aide")
        dialog.setFixedSize(500, 500)

        QLabel("<h1>Aide du jeu !</h1><p>Le but du jeu est de combler les trous en y plaçant les différentes pierres.</p><p>Vous pouvez vous déplacer en utilisant :</p><p> fléche haut ( ou 'z' ) pour aller vers le haut;</p><p> fléche bas ( ou 's' ) pour aller vers le bas;</p><p> fléche gauche ( ou 'q' ) pour aller vers la gauche;</p><p> fléche droit ( ou 'd' ) pour aller vers la droite;</p>", parent=dialog)

        dialog.exec_()

