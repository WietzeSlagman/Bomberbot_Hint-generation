'''
    File: parse_json.py
    Authors: Joeri Bes, Haischel Dabian, Jim Buissink, Sebastiaan Joustra and
        Wietze Slagman
    Date: 16/06/2016
    Python version: 3.x
    Created for the Bomberbot coorporation
---------------------------------------------
    File description:
    This file contains functions in order to parse the json files from 
    the puzzles. 
'''


import json

def get_tiles(filename):
    '''Returns the tiles of the json file.'''
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data["tiles"]

def get_dimensions(filename):
    '''Returns the dimensions of the grid.'''
    with open(filename) as data_file:    
        data = json.load(data_file)
    return [data["dimension"]["cols"], data["dimension"]["rows"]]

def get_pos_player(filename):
    '''Returns the start location of the user.'''
    with open(filename) as data_file:    
        data = json.load(data_file)
    return [data["posPlayer"]["x"], data["posPlayer"]["y"]]

def get_best_solutions(filename):
    '''Returns the best solution as an integer.'''
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data["solutions"]["best"]

def get_dir_player(filename):
    '''Returns the start direction of the user, if there's no 
    start direction given, the direction is downwards.
    '''
    with open(filename) as data_file:
        data = json.load(data_file)
    try:
        return data["dirPlayer"]
    except KeyError:
        return "down"

def get_demo(mission,level):
    '''Returns a string of moves from the demo'''
    with open("Json/demo.json") as data_file:
        data = json.load(data_file)
    try:
        return [data[str(mission)][str(level)]["moveList"], \
            data[str(mission)][str(level)]["goalsCollected"]]
    except KeyError:
        return None

def has_hammer(filename):
    '''Returns if the user has the possibility of using a hammer.'''
    with open(filename) as data_file:    
        data = json.load(data_file)
    try:
        return data["hammer"]
    except KeyError:
        return False



