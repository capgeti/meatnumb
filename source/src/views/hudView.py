import bge
from src import playerController
import src.bgui as bgui
from src.views.defaultView import DefaultView


class HudView(DefaultView):
    def __init__(self):
        DefaultView.__init__(self)

        self.ptNormal = int(bge.render.getWindowHeight() / 12)
        self.ptGross = int(bge.render.getWindowHeight() / 9)
        self.ptSehrGross = int(bge.render.getWindowHeight() / 8)

        width = bge.render.getWindowWidth()
        height = bge.render.getWindowHeight()

        aspect = width / height

        self.itemcount = 3
        self.items = []

        self.createHPView(aspect)
        self.createMunintionView(aspect)
        self.createItemList(aspect)
        self.createMainMenu()

    def createMainMenu(self):
        self.gameMenuFrame = bgui.Frame(self, "gameMenuFrame", size=[1, 1], sub_theme="dark")
        self.gameMenu = bgui.Frame(self.gameMenuFrame, "gameMenu", size=[0.3, 0.7], pos=[0.35, 0.15], border=1)
        self.resumeGameButton = bgui.FrameButton(self.gameMenu, 'resumeGameButton', text='Weiter',
            pt_size=self.ptNormal, size=[0.7, 0.1], pos=[0.3, 0.75], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX);
        self.resumeGameButton.on_click = self.resumeGame
        self.mainMenuButton = bgui.FrameButton(self.gameMenu, 'mainMenuButton', text='Hauptmenü',
            pt_size=self.ptNormal, size=[0.7, 0.1], pos=[0.3, 0.55], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX);
        self.mainMenuButton.on_click = self.showMainMenu
        self.gameMenuFrame.visible = False

    def createHPView(self, aspect):
        self.hpFrame = bgui.Frame(self, "hpFrame", border=1, pos=[0.01, 0.01], size=[0.1, 0.1 * aspect],
            sub_theme="transp")
        self.hpOben = bgui.Frame(self.hpFrame, "hpOben", pos=[0, 0.5], size=[1, 0.5])
        bgui.Label(self.hpOben, "hptext", text="Leben:", pt_size=self.ptGross, pos=[0.05, 0],
            options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERY)
        self.hpUnten = bgui.Frame(self.hpFrame, "hpUnten", pos=[0, 0], size=[1, 0.5])
        self.hpAnzeige = bgui.Label(self.hpUnten, "hpAnzeige", text="100", pt_size=self.ptSehrGross,  pos=[0.05, 0],
            options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERY)

    def createItemList(self, aspect):
        self.itemFrame = bgui.Frame(self, "itemFrame", size=[0.225, 0.068 * aspect], pos=[0.3875, 0.01],
            sub_theme="transp")

        for i in range(self.itemcount):
            itemBox = ItemView(i, self.itemFrame, "item" + str(i), size=[0.3, 1], pos=[0 + (i * 0.35), 0])
            itemBox.on_click = self.selectItem
            self.items.append(itemBox)

    def update_keyboard(self, key, is_shifted):
        if key == 218: # ESC
            self.gameMenuFrame.visible = not self.gameMenuFrame.visible

        for i in range(self.itemcount):
            if key == str(i + 1):
                self.selectItem(self.items[i])

        if key == "q":
            playerController.dropCurrentWeapon()

    def resumeGame(self, button):
        self.gameMenuFrame.visible = False

    def showMainMenu(self, button):
        bge.logic.addScene("Main", 0)
        bge.logic.getCurrentScene().end()

    def selectItem(self, item):
        for i in range(self.itemcount):
            self.items[i].activeImage.visible = False
        item.activeImage.visible = True
        playerController.setWaffenSlot(item.slot)

    def main(self):
        DefaultView.main(self)

        weapons = playerController.player['weapons']
        for i in range(self.itemcount):
            item = self.items[i].itemImage
            itemImage = item.image
            if weapons[i]:
                path = "textures/" + weapons[i] + ".png"
                if itemImage != path:
                    item.visible = True
                    item.update_image(path)
            elif item.image:
                item.visible = False
                item.image = None

    def createMunintionView(self, aspect):
        self.muniFrame = bgui.Frame(self, "hpFrame", border=1, pos=[0.01, 0.01], size=[0.1, 0.1 * aspect],
            sub_theme="transp")
        self.hpOben = bgui.Frame(self.hpFrame, "hpOben", pos=[0, 0.5], size=[1, 0.5])
        bgui.Label(self.hpOben, "hptext", text="Leben:", pt_size=self.ptGross, pos=[0.05, 0],
            options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERY)
        self.hpUnten = bgui.Frame(self.hpFrame, "hpUnten", pos=[0, 0], size=[1, 0.5])
        self.hpAnzeige = bgui.Label(self.hpUnten, "hpAnzeige", text="100", pt_size=self.ptSehrGross,  pos=[0.05, 0],
            options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERY)

    pass


class ItemView(bgui.Image):
    def __init__(self, slot, parent, name, img="textures/itemEmpty.png", size=None, pos=None):
        if not pos: pos = [0, 0]
        if not size: size = [0, 0]
        bgui.Image.__init__(self, parent, name, img=img, size=size, pos=pos)

        self.slot = slot

        self.hoverImage = bgui.Image(self, "hover_" + name, size=[1, 1], img="textures/itemHover.png")
        self.hoverImage.visible = False

        self.activeImage = bgui.Image(self, "active_" + name, size=[1, 1], img="textures/itemActive.png")
        self.activeImage.visible = False

        self.itemImage = bgui.Image(self, "itemImage_" + name, size=[1, 1], img="")
        self.itemImage.visible = False

        self.on_mouse_enter = self.showHoverImage
        self.on_mouse_exit = self.hideHoverImage

    def showHoverImage(self, image):
        self.hoverImage.visible = True
        playerController.lockShoot = True

    def hideHoverImage(self, image):
        self.hoverImage.visible = False
        playerController.lockShoot = False

