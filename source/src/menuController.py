from src.views.highScoreView import HighScoreView
from src.views.hudView import HudView
from src.views.mainView import MainView

__author__ = 'capgeti'

def handleView(cont, ViewObject):
    mainEmpty = cont.owner
    if not mainEmpty.get("menuInit"):
        mainEmpty['menuInit'] = ViewObject()
    mainEmpty['menuInit'].main()


def mainMenu(cont):
    handleView(cont, MainView)


def highScoreMenu(cont):
    handleView(cont, HighScoreView)

def hudView(cont):
    handleView(cont, HudView)