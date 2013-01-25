import bge
import src.bgui as bgui
from src.views.defaultView import DefaultView


class MainView(DefaultView):
    def __init__(self):
        DefaultView.__init__(self)

        self.ptNormal = int(bge.render.getWindowHeight() / 10)
        self.ptGross = int(bge.render.getWindowHeight() / 3)
        self.ptKlein = int(bge.render.getWindowHeight() / 20)

        self.bgImage = bgui.Image(self, "bgImage", img="textures/bg.JPG", size=[1, 1])

        bgui.Label(self.bgImage, "mainLabel", pos=[0.4, 0.5], text="Meat-NUMB", pt_size=self.ptGross,
            options=bgui.BGUI_DEFAULT)
        bgui.Label(self.bgImage, "cLabel", pos=[0, 0], text="(c) 2013, capgeti, v0.9", pt_size=self.ptKlein)

        self.gameMenu = bgui.Frame(self.bgImage, "gameMenu", size=[0.3, 0.7], pos=[0.02, 0.15], border=1)

        self.newGameButton = bgui.FrameButton(self.gameMenu, 'newGameButton', text='Neues Spiel', pt_size=self.ptNormal,
            size=[0.7, 0.1], pos=[0.3, 0.75], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
        self.newGameButton.on_click = self.startNewGame

        self.highScoreButton = bgui.FrameButton(self.gameMenu, 'highScoreButton', text='Highscore',
            pt_size=self.ptNormal,
            size=[0.7, 0.1], pos=[0.3, 0.55], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
        self.highScoreButton.on_click = self.showHighScoreMenu

        self.exitButton = bgui.FrameButton(self.gameMenu, 'exitButton', text='Beenden', pt_size=self.ptNormal,
            size=[0.7, 0.1],
            pos=[0.3, 0.35], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
        self.exitButton.on_click = self.exitGame

    def exitGame(self, button):
        bge.logic.endGame()

    def startNewGame(self, button):
        bge.logic.addScene("lvl1", 0)
        bge.logic.getCurrentScene().end()

    def showHighScoreMenu(self, button):
        bge.logic.addScene("highScore", 0)
        bge.logic.getCurrentScene().end()