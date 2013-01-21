from src import waveController
from src.views.hudView import HudView

__author__ = 'capgeti'

def init(cont):
    handle  = cont.owner
    handle['view'] = HudView()

    waveController.init(handle)

def gameLoop(cont):
    handle = cont.owner

    viewHandle = handle['view']
    viewHandle.main()

    waveController.calcSpawnTime(handle)