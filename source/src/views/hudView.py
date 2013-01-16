import bge
import src.bgui as bgui
from src.views.defaultView import DefaultView


class HudView(DefaultView):
    def __init__(self):
        DefaultView.__init__(self)

        self.ptNormal = int(bge.render.getWindowHeight() / 10)
        self.ptGross = int(bge.render.getWindowHeight() / 8)
        self.ptSehrGross = int(bge.render.getWindowHeight() / 7)

        width = bge.render.getWindowWidth()
        height = bge.render.getWindowHeight()

        aspect = width / height

        self.hpFrame = bgui.Frame(self, "hpFrame", border=1, pos=[0.01, 0.01], size=[0.1, 0.1 * aspect],
            sub_theme="transp")

        self.hpOben = bgui.Frame(self.hpFrame, "hpOben", pos=[0, 0.5], size=[1, 0.5])
        bgui.Label(self.hpOben, "hptext", text="Leben:", pt_size=self.ptGross,
            options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERED)

        self.hpUnten = bgui.Frame(self.hpFrame, "hpUnten", pos=[0, 0], size=[1, 0.5])
        self.hpAnzeige = bgui.Label(self.hpUnten, "hpAnzeige", text="100", pt_size=self.ptSehrGross,
            options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERED)

        self.gameMenuFrame = bgui.Frame(self, "gameMenuFrame", size=[1, 1], sub_theme="dark")
        self.gameMenu = bgui.Frame(self.gameMenuFrame, "gameMenu", size=[0.3, 0.7], pos=[0.35, 0.15], border=1)

        self.resumeGameButton = bgui.FrameButton(self.gameMenu, 'resumeGameButton', text='Weiter',
            pt_size=self.ptNormal, size=[0.7, 0.1], pos=[0.3, 0.75], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX);
        self.resumeGameButton.on_click = self.resumeGame

        self.mainMenuButton = bgui.FrameButton(self.gameMenu, 'mainMenuButton', text='Hauptmenü',
            pt_size=self.ptNormal, size=[0.7, 0.1], pos=[0.3, 0.55], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX);
        self.mainMenuButton.on_click = self.showMainMenu

        self.gameMenuFrame.visible = False


    def update_keyboard(self, key, is_shifted):
        if key == 218: # ESC
            self.gameMenuFrame.visible = not self.gameMenuFrame.visible

    def resumeGame(self, button):
        self.gameMenuFrame.visible = False

    def showMainMenu(self, button):
        bge.logic.addScene("Main", 0)
        bge.logic.getCurrentScene().end()



