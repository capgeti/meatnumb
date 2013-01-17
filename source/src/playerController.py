from itertools import groupby

import bge
from mathutils import Vector


__author__ = 'capgeti'

player = None
currentWeaponObject = None
lockShoot = False

def setCurrentWeapon(weaponName):
    scene = bge.logic.getCurrentScene()
    weaponEmpty = scene.objects['waffenFokus']
    global currentWeaponObject
    currentWeaponObject = scene.addObject(weaponName, weaponEmpty)
    currentWeaponObject.setParent(weaponEmpty)


def removeCurrentWeapon():
    global currentWeaponObject
    if currentWeaponObject:
        currentWeaponObject.endObject()
    currentWeaponObject = None


def init(cont):
    global player
    player = cont.owner
    player['weapons'] = [None for i in range(3)]
    player['currentWeaponSlot'] = -1
    player['hp'] = 100
    player['speed'] = 5


def dropCurrentWeapon():
    global currentWeaponObject

    if not currentWeaponObject:
        return

    try:
        currentslot = player['currentWeaponSlot']
        player['weapons'][currentslot] = None
        currentWeaponObject.removeParent()
        currentWeaponObject.orientation = player.orientation
        currentWeaponObject.applyForce((0, 160, 50), True)
        currentWeaponObject = None
    except IndexError:
        return


def updatePlayerLookAt(cont):
    over = cont.sensors["overAny"]
    if over.positive and not "useable" in over.hitObject:
        cont.owner.position = over.hitPosition


def move(cont):
    keyboard = bge.logic.keyboard.events

    w = keyboard[bge.events.WKEY] == 2
    a = keyboard[bge.events.AKEY] == 2
    s = keyboard[bge.events.SKEY] == 2
    d = keyboard[bge.events.DKEY] == 2

    bones = player.children['playerBones']

    if w or s or a or d:
    #        bge.logic.sendMessage("playAction", "gehen", "playerBones")
        bones.playAction("gehenBeine", 1, 15, blendin=5, layer=0, play_mode=1)
        if not currentWeaponObject:
            bones.playAction("gehenArme", 1, 15, blendin=5, layer=1, play_mode=1)

        speed = player.get("speed", 0)

        x = speed if d else -speed if a else 0
        y = speed if w else -speed if s else 0
        if (w or s) and (a or d):
            x /= 1.3
            y /= 1.3

        player["vel"] = Vector((x, y, 0))
    else:
        bones.playAction("stehenBeine", 1, 1, blendin=2, layer=0, play_mode=1)
        if not currentWeaponObject:
            bones.playAction("stehenArme", 1, 1, blendin=2, layer=1, play_mode=1)

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

    if click.positive and currentWeaponObject and not lockShoot:
        player = cont.owner
        bones = player.children['playerBones']
        bones.playAction("schuss", 1, 5, blendin=2, layer=1, play_mode=0)


def setWaffenSlot(slot, checkCurrent=True):
    if slot == player['currentWeaponSlot'] and checkCurrent:
        return

    removeCurrentWeapon()

    try:
        newWeaponName = player['weapons'][slot]

        bones = player.children['playerBones']
        if not newWeaponName:
            if currentWeaponObject:
                bones.playAction("waffetragen", 5, 1, blendin=2, layer=2, play_mode=0)
            return

        setCurrentWeapon(newWeaponName)
        bones.playAction("waffetragen", 1, 5, blendin=2, layer=1, play_mode=0)
    except IndexError:
        pass
    finally:
        player['currentWeaponSlot'] = slot


def pickUp(cont):
    collision = cont.sensors['colli']
    if not collision.positive:
        return

    pickUpObject = collision.hitObject
    if pickUpObject.get("useable") == "weapon" and len([e for e in player['weapons'] if not e]) > 0:
        freeSlot = player['weapons'].index(None)
        player['weapons'][freeSlot] = pickUpObject.name
        if player['currentWeaponSlot'] == freeSlot:
            setWaffenSlot(player['currentWeaponSlot'], checkCurrent=False)
        pickUpObject.endObject()


















