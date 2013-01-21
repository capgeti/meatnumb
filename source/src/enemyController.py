from src import playerController

__author__ = 'capgeti'


def hitPlayer(cont):
    enemy = cont.owner

    hit = cont.sensors['hitPlayer']
    timer = cont.sensors['hitPlayer']

    if hit.positive and enemy['timer'] > enemy['abklingzeit']:
        playerController.player['hp'] -= enemy['damage']
        enemy['timer'] = 0
        print("hit!")
