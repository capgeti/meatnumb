import bge
from mathutils import Vector

__author__ = 'capgeti'

def init(cont):
    player = cont.owner
    scene = bge.logic.getCurrentScene()

    waffenEmpty = scene.objects['waffenFokus']

    pistole = scene.addObject("weapon01", waffenEmpty)
    pistole.setParent(waffenEmpty)
    player['waffe0'] = pistole

def updatePlayerLookAt(cont):
    over = cont.sensors["overAny"]
    if over.positive:
        cont.owner.position = over.hitPosition


def move(cont):
    keyboard = bge.logic.keyboard.events

    w = keyboard[bge.events.WKEY] == 2
    a = keyboard[bge.events.AKEY] == 2
    s = keyboard[bge.events.SKEY] == 2
    d = keyboard[bge.events.DKEY] == 2

    player = cont.owner
    bones = player.children['playerBones']

    if w or s or a or d:
        bones.playAction("walkingLegs", 1, 15, blendin=5, layer=1, play_mode=1)

        speed = player.get("speed", 0)

        x = speed if d else -speed if a else 0
        y = speed if w else -speed if s else 0
        if (w or s) and (a or d):
            x /= 1.3
            y /= 1.3

        player["vel"] = Vector((x, y, 0))
    else:
        bones.playAction("standingLegs", 1, 1, blendin=2, layer=1, play_mode=1)

    if not player.get("vel"):
        return

    player["vel"] *= 0.5

    velNew = player["vel"]
    velNew.z = player.getLinearVelocity()[2]

    player.setLinearVelocity(velNew)


def handleZoom(cont):
    mouseUp = cont.sensors['up'].positive
    mouseDown = cont.sensors['down'].positive

    cameraRotater = cont.owner
    currZoom = cameraRotater.get("zoom", 0.7)

    neu = currZoom + (0.2 if mouseDown else -0.2 if mouseUp else 0)
    neu = 1.2 if neu > 1.2 else 0.2 if neu < 0.2 else neu
    cameraRotater['zoom'] = neu

    cameraRotater.scaling = (neu, neu, neu)


def shoot(cont):
    click = cont.sensors['left']

    if click.positive:
        player = cont.owner
        bones = player.children['playerBones']
        bones.playAction("schuss", 1, 5, layer=2, play_mode=0)