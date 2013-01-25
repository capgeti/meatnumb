import bge
import src.bgui as bgui
from src.views.defaultView import DefaultView


class HighScoreView(DefaultView):
    def __init__(self):
        DefaultView.__init__(self)

        self.ptNormal = int(bge.render.getWindowHeight() / 10)
        self.ptGross = int(bge.render.getWindowHeight() / 3)
        self.ptKlein = int(bge.render.getWindowHeight() / 20)

        self.bgImage = bgui.Image(self, "bgImage", img="textures/bg.JPG", size=[1, 1])

        bgui.Label(self.bgImage, "mainLabel", pos=[0.4, 0.5], text="Highscore!  ", pt_size=self.ptGross,
            options=bgui.BGUI_DEFAULT)
        bgui.Label(self.bgImage, "cLabel", pos=[0, 0], text="(c) 2013, capgeti, v0.9", pt_size=self.ptKlein)

        self.gameMenu = bgui.Frame(self.bgImage, "gameMenu", size=[0.3, 0.7], pos=[0.02, 0.15], border=1)

        self.backButton = bgui.FrameButton(self.gameMenu, 'backButton', text='Zurück', pt_size=self.ptNormal,
            size=[0.7, 0.1], pos=[0.3, 0.75], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
        self.backButton.on_click = self.forBack

        bge.logic.loadGlobalDict()

        if not "highScore" in bge.logic.globalDict:
            bge.logic.globalDict['highScore'] = list()

        scores = bge.logic.globalDict['highScore']
        if not scores:
            return

        scores.sort(key=lambda tup: tup[1])
        scores.reverse()

        for i, score in enumerate(scores):
            wer = str(i+1) + ") " + score[0] + ": " + str(score[1])
            bgui.Label(self.bgImage, "highScore" + str(i), text=wer, pt_size=self.ptNormal-13, pos=[0.1, 0.6 - (i * 0.05)])

    def forBack(self, button):
        bge.logic.addScene("Main", 0)
        bge.logic.getCurrentScene().end()