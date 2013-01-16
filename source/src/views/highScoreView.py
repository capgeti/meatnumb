import bge
import src.bgui as bgui
from src.views.defaultView import DefaultView


class HighScoreView(DefaultView):
    def __init__(self):
        DefaultView.__init__(self)

        self.pt_size = int(bge.render.getWindowHeight() / 20)

        self.backButton = bgui.FrameButton(self, 'backButton', text='Zurück', pt_size=self.pt_size,
            size=[0.3, 0.1], pos=[0.3, 0.75], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
        self.backButton.on_click = self.forBack


    def forBack(self, button):
        bge.logic.addScene("Main", 0)
        bge.logic.getCurrentScene().end()