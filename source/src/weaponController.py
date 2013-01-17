__author__ = 'capgeti'

def reNewPickUp(cont):
    if cont.sensors['away'].positive:
        weapon = cont.owner
        weapon['pickupable'] = 1

