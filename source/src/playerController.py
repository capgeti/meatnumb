import random
import bge
import aud
from mathutils import Vector
from src import item, waveController

__author__ = 'capgeti'

player = None

device = aud.device()

def playSound(file):
    device.play(aud.Factory("sounds/" + file))


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
    player['hp'] = 100
    player['speed'] = 5
    player['currentWeaponObject'] = None
    player['currentWeapon'] = None
    player['spawnTimer'] = 1000
    player['lockShoot'] = False
    player['isTot'] = False
    player['points'] = 0


def dropCurrentWeapon():
    if player['isTot'] or not player['currentWeapon']: return

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

    if player['isTot']:
        if not bones.isPlayingAction(2):
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
        bones.playAction("sterben", 1, 11, blendin=4, layer=2, play_mode=0, priority=0)
        bones.stopAction(0)
        bones.stopAction(1)


def handleZoom(cont):
    if player['isTot']: return
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


def drawShootLine(shootFrom, shootTo, startCount, endCount, color):
    diff = shootTo - shootFrom
    start = shootFrom + (diff * startCount)
    ende = shootFrom + (diff * endCount)
    bge.render.drawLine(start, ende, color)


def shoot(cont):
    click = cont.sensors['left']

    if not click.positive or not player['currentWeapon'] or player['lockShoot'] or not player['currentWeapon'].schuss:
        if not player['currentWeapon'].schuss:
            playSound("leer.wav")
        return

    if player['isTot']: return

    if player['currentWeapon'].objName == "weapon01":
        playSound("pistol.wav")
    else:
        playSound("mp.wav")

    bones = player.children['playerBones']
    bones.playAction("schuss", 1, 5, blendin=2, layer=1, play_mode=0)

    scene = bge.logic.getCurrentScene()
    obj = scene.addObject("ShootSplash", player['currentWeaponObject'].children[0], 1)
    obj.setParent(player['currentWeaponObject'])

    shootFrom = player.children['ShootFrom']
    shootTo = scene.objects['playerLookAt']

    dist = 1000
    ray = shootFrom.rayCast(shootTo, None, dist)

    dist = shootFrom.getDistanceTo(ray[1]) * 3
    obj = scene.addObject("BulletHole", ray[0], 100)
    obj.alignAxisToVect(ray[2], 1, 1)
    obj.worldPosition = ray[1]
    obj.setParent(ray[0])

    player['points'] -= 1
    if player['points'] < 0:
        player['points'] = 0

    hitObject = ray[0]
    if "enemy" in hitObject:
        hitObject['hp'] -= player['currentWeapon'].damage

        if hitObject['hp'] <= 0 and not hitObject.get("tot"):
            enemies = waveController.currentEnemies
            del enemies[enemies.index(hitObject)]
            player['points'] += 10

            i = random.randint(1, 5)
            if i == 3:
                i2 = random.randint(1, 2)
                if i2 == 1:
                    scene.addObject("ammoPistole", hitObject)
                else:
                    scene.addObject("ammoMp", hitObject)

            hitObject['tot'] = True
            hitObject.suspendDynamics()

    froW = shootFrom.worldPosition.copy()

    start = random.random() * 0.2
    endFirst = start + (random.random() * 0.3)
    endFirst2 = endFirst + (random.random() * 0.5)

    drawShootLine(froW, ray[1], start, endFirst, (1, 1, 0.5))
    drawShootLine(froW, ray[1], endFirst2, 1, (1, 1, 0.5))

    player['currentWeapon'].schuss -= 1

    checkReload()


def checkReload():
    if player['currentWeapon'] and player['currentWeapon'].schuss <= 0:
        player['currentWeapon'].magazine -= 1
        if player['currentWeapon'].magazine < 0:
            player['currentWeapon'].magazine = 0
            return
        player['currentWeapon'].schuss = player['currentWeapon'].schusskapa


def setWaffenSlot(slot, checkCurrent=True):
    if player['isTot']: return

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
    if player['isTot']: return

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
        checkReload()


def getWeaponByName(name):
    for weapon in player['weapons']:
        if weapon and weapon.objName == name:
            return weapon
    return None


















