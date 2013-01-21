from src.views.highScoreView import HighScoreView
from src.views.mainView import MainView

__author__ = 'capgeti'

view = MainView()

def gameLoop(cont):
    view.main()


def showHighScoreView():
    global view
    view = HighScoreView()


def showMainView():
    global view
    view = MainView()