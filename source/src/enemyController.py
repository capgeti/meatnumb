import bge
from src import playerController

__author__ = 'capgeti'

def hitPlayer(cont):
    enemy = cont.owner
    hit = cont.sensors['hitPlayer']
    if hit.positive and enemy['timer'] > enemy['abklingzeit']:
        playerController.player['hp'] -= enemy['damage']
        if playerController.player['hp'] < 0:
            playerController.player['hp'] = 0
        enemy['timer'] = 0


def init(cont):
    steering = cont.actuators['Steering']

    steering.target = "playerBox"
    steering.navmesh = bge.logic.getCurrentScene().objects['Navmesh']

    cont.activate(steering)