'''
    File: objects.py
    Authors: Joeri Bes, Haischel Dabian, Jim Buissink, Sebastiaan Joustra and
        Wietze Slagman
    Date: 16/06/2016
    Python version: 3.x
    Created for the Bomberbot coorporation
---------------------------------------------
    File description:
    This file contains all the objects used by the main program to create
    a playable game world on which we can run our solver
'''
class Tile:
    def __init__(self, slideable, obj, x, y):
        self.slideable = slideable
        self.obj = obj
        self.x_coord = x
        self.y_coord = y

        # Values used by the A* algorithm to calculate the costs
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def is_walkable(self):
        '''Checks if the tiles is walkable.'''
        if self.obj is not None:
            if self.obj.__class__.__name__ is 'Star' or \
                self.obj.__class__.__name__ is 'Hammer':
                return True
            return False
        return True

    def has_object(self):
        '''Checks if the tile has an object.'''
        if self.obj is not None:
            return True     
        return False

    def get_object_name(self):
        '''Returns the name of the object.'''
        return self.obj.__class__.__name__

    def remove_object(self):
        '''Removes the object from the tile.'''
        self.has_object = False
        self.obj = None

class Star:
    def __init__(self):
        self.passed = False
        self.destroyable = False

class Hammer:
    def __init__(self):
        self.passed = False
        self.destroyable = False

class Ruby:
    def __init__(self, destroyable=True, destroyed=False):
        self.destroyable = destroyable
        self.destroyed = destroyed
        self.destroy_cost = 0

    def destroy(self):
        '''Destroy the object if the object is destroyable and not destroyed.'''
        if self.destroyable and not self.destroyed:
            self.destroyed = True
            return True
        return False

class Brick:
    def __init__(self, destroyable, destroyed=False):
        self.destroyable = destroyable
        self.destroyed = destroyed
        self.destroy_cost = 0

    def destroy(self):
        '''Destroy the object if the object is destroyable and not destroyed.'''
        if self.destroyable and not self.destroyed:
            self.destroyed = True
            return True
        return False