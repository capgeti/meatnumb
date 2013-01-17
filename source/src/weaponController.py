__author__ = 'capgeti'

def reNewPickUp(cont):
    print("PickUp: ", cont.sensors['away'].positive)
    if cont.sensors['away'].positive:
        weapon = cont.owner
        weapon['pickupable'] = 1

