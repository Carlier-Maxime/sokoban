# importation des librairie nécessaire
from os import walk
from PyQt5.QtWidgets import *
from controllers.crtlTheme import CrtlTheme


class ThemeView(QMainWindow):
    def __init__(self, view):
        super(ThemeView, self).__init__()
        self.__view = view
        self.setWindowTitle("Settings - Theme")
        self.setFixedSize(340, 450)

        # Apercu + comboBox (central widget)
        w = CrtlTheme(self)
        w.setLayout(QVBoxLayout(w))
        w.setStyleSheet("border: 1px solid gray")

        self.__apercu = QWidget()
        self.__apercu.setLayout(QGridLayout(self.__apercu))
        self.__apercu.setFixedSize(320, 320)
        self.__apercu.setStyleSheet("background-image: url(images/" + view.getTheme() + "/apercu.png)")
        w.layout().addWidget(self.__apercu)

        HBox1 = QWidget()
        HBox1.setLayout(QHBoxLayout(HBox1))
        HBox1.layout().addWidget(QLabel("Theme :"))
        self.__ComboBox = QComboBox()
        for theme in next(walk("images"))[1]:
            self.__ComboBox.addItem(theme)
        self.__ComboBox.setCurrentText(view.getTheme())
        self.__ComboBox.currentTextChanged.connect(self.updateApercu)
        self.__ComboBox.setFixedSize(225, 25)
        HBox1.layout().addWidget(self.__ComboBox)
        HBox1.setFixedSize(HBox1.layout().totalMinimumSize())
        w.layout().addWidget(HBox1)
        self.setCentralWidget(w)

        # statut bar
        bar = self.statusBar()
        bar.setStyleSheet("border: 1px solid gray")
        buttonApply = QPushButton("Appliquer")
        buttonApply.clicked.connect(self.apply)
        buttonCancel = QPushButton("Annuler")
        buttonCancel.clicked.connect(self.cancel)
        bar.addPermanentWidget(buttonApply)
        bar.addPermanentWidget(buttonCancel)

    def changeTheme(self, inc: int = 0):
        theme = self.__ComboBox.currentText()
        for i in range(self.__ComboBox.count()):
            if self.__ComboBox.itemText(i) == theme:
                if i+inc == self.__ComboBox.count():
                    self.__ComboBox.setCurrentText(self.__ComboBox.itemText(0))
                elif i+inc == -1:
                    self.__ComboBox.setCurrentText(self.__ComboBox.itemText(self.__ComboBox.count()-1))
                else:
                    self.__ComboBox.setCurrentText(self.__ComboBox.itemText(i+inc))
                break
        self.updateApercu()

    def updateApercu(self):
        self.__apercu.setStyleSheet("background-image: url(images/" + self.__ComboBox.currentText() + "/apercu.png)")

    def cancel(self):
        self.__view.closeSecondView()

    def apply(self):
        self.__view.setTheme(self.__ComboBox.currentText())
        self.__view.updateView()
        self.cancel()

    def closeEvent(self, event):
        self.centralWidget().releaseKeyboard()
        super(QMainWindow, self).closeEvent(event)
