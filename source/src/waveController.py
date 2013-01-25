import time
import random
import threading
import bge
import copy


__author__ = 'capgeti'


class SpawnUtil(threading.Thread):

    def __init__(self, waveData, level):
        super().__init__()
        self.waveData = copy.deepcopy(waveData)
        self.level = level

    def spawnMob(self, enemy):
        scene = bge.logic.getCurrentScene()
        enemyObject = scene.addObject(enemy, getRandomSpawnPoint())
        currentEnemies.append(enemyObject)

    def run(self):
        randomMobs = self.waveData[0]

        global fullSpawned
        fullSpawned = False

        for i in range(sum(randomMobs.values())):
            enemy = random.choice(list(randomMobs.keys()))
            self.spawnMob(enemy)
            randomMobs[enemy] -= 1

            if randomMobs[enemy] == 0:
                del randomMobs[enemy]

            spawnTime = 1 - min(0.7, self.level / 50)
            time.sleep(spawnTime)

        if len(self.waveData) > 1:
            self.spawnMob(self.waveData[1])

        fullSpawned = True


spawnPoints = None
spawnTime = None
spawnTimer = None
timerInit = None
waveCounter = None
fullSpawned = None

currentEnemies = []

def init(handle):
    global spawnTime, spawnTimer, waveCounter, fullSpawned, currentEnemies, spawnPoints

    spawnPoints = list()
    spawnTime = 3
    spawnTimer = spawnTime
    waveCounter = 0
    fullSpawned = False

    currentEnemies = []

    scene = bge.logic.getCurrentScene()
    handle['spawnTimer'] = 0

    for obj in scene.objects:
        if "spawnPoint" in obj.name:
            spawnPoints.append(obj)
            scene.addObject("alienSpawn", obj)


def getRandomSpawnPoint():
    spawnNumber = random.randint(0, len(spawnPoints) - 1)
    return spawnPoints[spawnNumber]


def calcSpawnTime(handle):
    global spawnTimer, fullSpawned

    if not currentEnemies and fullSpawned:
        handle['spawnTimer'] = 0
        spawnTimer = 1
        fullSpawned = False

    if spawnTimer <= 0:
        return

    spawnTimer = spawnTime - int(handle['spawnTimer'])

    if spawnTimer == 0:
        global waveCounter
        SpawnUtil([{"enemy01": int((waveCounter + 1) * 3)}], waveCounter).start()
        waveCounter += 1


