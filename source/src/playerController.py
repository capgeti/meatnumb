import random

import bge
from mathutils import Vector
from src import item, waveController

__author__ = 'capgeti'

player = None

def setCurrentWeapon(newWeapon):
    scene = bge.logic.getCurrentScene()
    weaponEmpty = scene.objects['waffenFokus']

    player['currentWeapon'] = newWeapon
    player['currentWeaponObject'] = scene.addObject(newWeapon.objName, weaponEmpty)
    player['currentWeaponObject'].setParent(weaponEmpty)

    player.sensors['left'].frequency = player['currentWeapon'].abklingzeit


def removeCurrentWeapon():
    if player['currentWeapon']:
        player['currentWeaponObject'].endObject()
    player['currentWeaponObject'] = None
    player['currentWeapon'] = None


def init(cont):
    global player
    player = cont.owner
    player['weapons'] = [None for i in range(3)]
    player['currentWeaponSlot'] = -1
    player['hp'] = 4
    player['speed'] = 5
    player['currentWeaponObject'] = None
    player['currentWeapon'] = None
    player['lockShoot'] = False
    player['isTot'] = False
    player['kills'] = 0


def dropCurrentWeapon():
    if not player['currentWeapon']:
        return

    try:
        currentslot = player['currentWeaponSlot']
        player['weapons'][currentslot] = None

        player['currentWeaponObject'].removeParent()
        player['currentWeaponObject'].orientation = player.orientation
        player['currentWeaponObject'].applyForce((0, 160, 50), True)
        player['currentWeaponObject']['weapon'] = player['currentWeapon']

        player['currentWeaponObject'] = None
        player['currentWeapon'] = None
    except IndexError:
        return


def updatePlayerLookAt(cont):
    if player['isTot']: return
    over = cont.sensors["overAny"]
    if over.positive and not "useable" in over.hitObject:
        cont.owner.position = over.hitPosition


def loop(cont):
    keyboard = bge.logic.keyboard.events

    w = keyboard[bge.events.WKEY] == 2
    a = keyboard[bge.events.AKEY] == 2
    s = keyboard[bge.events.SKEY] == 2
    d = keyboard[bge.events.DKEY] == 2

    bones = player.children['playerBones']

    if player['isTot'] and not bones.isPlayingAction(3):
        player.suspendDynamics()
        return


    if w or s or a or d:
        bones.playAction("gehenBeine", 1, 13, blendin=5, layer=0, play_mode=1)
        if not player['currentWeaponObject']:
            bones.playAction("gehenArme", 1, 13, blendin=5, layer=1, play_mode=1)

        speed = player.get("speed", 0)

        x = speed if d else -speed if a else 0
        y = speed if w else -speed if s else 0
        if (w or s) and (a or d):
            x /= 1.3
            y /= 1.3

        player["vel"] = Vector((x, y, 0))
    else:
        bones.playAction("stehenBeine", 1, 1, blendin=2, layer=0, play_mode=1)
        if not player['currentWeaponObject']:
            bones.playAction("stehenArme", 1, 1, blendin=2, layer=1, play_mode=1)

    if not player.get("vel"):
        return

    player["vel"] *= 0.5

    velNew = player["vel"]
    velNew.z = player.getLinearVelocity()[2]

    player.setLinearVelocity(velNew)

    if player['hp'] <= 0:
        player['lockShoot'] = True
        player['isTot'] = True
        bones.playAction("sterben", 1, 11, blendin=4, layer=3, play_mode=0)


def handleZoom(cont):
    mouseUp = cont.sensors['up'].positive
    mouseDown = cont.sensors['down'].positive

    cameraRotater = cont.owner
    currZoom = cameraRotater.get("zoom", 0.7)

    MIN = 0.2
    MAX = 2.2

    neu = currZoom + (MIN if mouseDown else -MIN if mouseUp else 0)
    neu = MAX if neu > MAX else MIN if neu < MIN else neu
    cameraRotater['zoom'] = neu

    cameraRotater.scaling = (neu, neu, neu)


def drawShootLine(startCount, endCount, color):
    shootFrom = player.children['ShootFrom']
    shootTo = shootFrom.children['ShootTo']

    froW = shootFrom.worldPosition.copy()
    toW = shootTo.worldPosition.copy()

    start = froW + ((toW - froW) * startCount)
    ende = start + ((toW - froW) * endCount)

    bge.render.drawLine(start, ende, color)


def shoot(cont):
    click = cont.sensors['left']

    if click.positive and player['currentWeapon'] and not player['lockShoot'] and player['currentWeapon'].schuss:
        bones = player.children['playerBones']
        bones.playAction("schuss", 1, 5, blendin=2, layer=1, play_mode=0)

        scene = bge.logic.getCurrentScene()
        obj = scene.addObject("ShootSplash", player['currentWeaponObject'].children[0], 1)
        obj.setParent(player['currentWeaponObject'])

        shootFrom = player.children['ShootFrom']
        shootTo = shootFrom.children['ShootTo']

        dist = 1000
        ray = shootFrom.rayCast(shootTo, None, dist)

        if ray[1]:
            dist = shootFrom.getDistanceTo(ray[0]) * 3
            obj = scene.addObject("BulletHole", ray[0], 100)
            obj.alignAxisToVect(ray[2], 1, 1)
            obj.worldPosition = ray[1]

            hitObject = ray[0]
            if "enemy" in hitObject:
                print("ha", hitObject['hp'])
                hitObject['hp'] -= player['currentWeapon'].damage
                if hitObject['hp'] <= 0:
                    enemies = waveController.currentEnemies
                    del enemies[enemies.index(hitObject)]
                    i = random.randint(1, 5)
                    if i == 3:
                        scene.addObject("ammoPistole", hitObject)
                    hitObject.endObject()

        r = 3 + random.random() * 4
        e = r + 2 + random.random() * 2
        e = e if e < dist else dist
        r = r if r < dist else dist
        drawShootLine(r, e, (1, 1, 0.5))

        r = 18 + random.random() * 10
        e = r + 2 + random.random() * 5
        e = e if e < dist else dist
        r = r if r < dist else dist
        drawShootLine(r, e, (1, 1, 0.4))

        player['currentWeapon'].schuss -= 1

        if player['currentWeapon'].schuss <= 0:
            player['currentWeapon'].magazine -= 1
            if player['currentWeapon'].magazine <= 0:
                return
            player['currentWeapon'].schuss = player['currentWeapon'].schusskapa


def setWaffenSlot(slot, checkCurrent=True):
    if slot == player['currentWeaponSlot'] and checkCurrent:
        return

    removeCurrentWeapon()

    try:
        newWeapon = player['weapons'][slot]

        bones = player.children['playerBones']
        if not newWeapon:
            if player['currentWeapon']:
                bones.playAction("waffetragen", 5, 1, blendin=2, layer=2, play_mode=0)
            return

        setCurrentWeapon(newWeapon)
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
        newWeapon = item.wrapper[pickUpObject.name]()
        if "weapon" in pickUpObject:
            newWeapon = pickUpObject['weapon']
        player['weapons'][freeSlot] = newWeapon
        if player['currentWeaponSlot'] == freeSlot:
            setWaffenSlot(player['currentWeaponSlot'], checkCurrent=False)
        pickUpObject.endObject()

    if pickUpObject.get("useable") == "ammo":
        weapon = getWeaponByName(pickUpObject["weapon"])
        if not weapon: return
        weapon.magazine += pickUpObject['magazines']
        pickUpObject.endObject()


def getWeaponByName(name):
    for weapon in player['weapons']:
        if weapon and weapon.objName == name:
            return weapon
    return None


















