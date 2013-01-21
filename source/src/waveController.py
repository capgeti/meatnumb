import time
import random
import threading

import bge


__author__ = 'capgeti'


class SpawnUtil(threading.Thread):
    locker = threading.Lock()

    def __init__(self, waveData):
        super().__init__()
        self.waveData = list(waveData)

    def spawnMob(self, enemy):
        SpawnUtil.locker.acquire()
        scene = bge.logic.getCurrentScene()
        enemyObject = scene.addObject(enemy, getRandomSpawnPoint())
        currentEnemies.append(enemyObject)
        SpawnUtil.locker.release()

    def run(self):
        randomMobs = self.waveData[0]

        SpawnUtil.locker.acquire()
        global fullSpawned
        fullSpawned = False
        SpawnUtil.locker.release()

        for i in range(sum(randomMobs.values())):
            enemy = random.choice(list(randomMobs.keys()))
            self.spawnMob(enemy)
            randomMobs[enemy] -= 1

            if randomMobs[enemy] == 0:
                del randomMobs[enemy]

            time.sleep(1)

        if len(self.waveData) > 1:
            self.spawnMob(self.waveData[1])


        SpawnUtil.locker.acquire()
        fullSpawned = True
        SpawnUtil.locker.release()


spawnPoints = list()
spawnTime = 2
spawnTimer = spawnTime
timerInit = time.time()
waveCounter = 0
fullSpawned = False

currentEnemies = []

waves = [
    [{"enemy01": 20}],
    [{"enemy01": 4}],
    [{"enemy01": 7}],
    [{"enemy01": 10}],
    [{"enemy01": 14}],
]


def init(handle):
    scene = bge.logic.getCurrentScene()
    handle['spawnTimer'] = 0

    for obj in scene.objects:
        if "spawnPoint" in obj.name:
            spawnPoints.append(obj)


def getRandomSpawnPoint():
    spawnNumber = random.randint(0, len(spawnPoints) - 1)
    return spawnPoints[spawnNumber]


def calcSpawnTime(handle):
    global spawnTimer, timerInit, fullSpawned

    if not currentEnemies and fullSpawned:
        handle['spawnTimer'] = 0
        spawnTimer = 1
        fullSpawned = False

    if spawnTimer <= 0:
        return

    spawnTimer = spawnTime - int(handle['spawnTimer'])

    if spawnTimer == 0:
        global waveCounter
        SpawnUtil(waves[waveCounter]).start()
        waveCounter += 1


