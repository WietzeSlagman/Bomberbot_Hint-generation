'''
    File: parse_output.py
    Authors: Joeri Bes, Haischel Dabian, Jim Buissink, Sebastiaan Joustra and
        Wietze Slagman
    Date: 16/06/2016
    Python version: 3.x
    Created for the Bomberbot coorporation
---------------------------------------------
    File description:
    This file contains the functions in order to generate commands from 
    a given path in coordinates. 

'''
import copy
from collections import Counter
import parse_json

def parse(path, start_tile, best_solution, rotations):
    '''This file gets called to translate a path list with tiles to a path
    list with game commands'''
    path_list = []
    direction_list = []
    for tile in path:
        path_list.append([tile.x_coord,tile.y_coord])

    prev_tile = [start_tile.x_coord, start_tile.y_coord]
    for tile in path_list:
        direction = get_direction(prev_tile, tile)
        direction_list.append(direction)

        prev_tile = tile.copy()

    new_dir_list = translate_same_locs(direction_list, best_solution, rotations)

    return new_dir_list

def get_direction(prev_tile, current_tile):
    '''Returns the direction of the bomberbot'''
    [x1, y1] = prev_tile
    [x2, y2] = current_tile

    if x2 > x1:
        direction = "right"
    elif x2 < x1:
        direction = "left"
    elif y2 > y1:
        direction = "down"
    elif y2 < y1:
        direction = "up"
    elif x1 == x2 and y1 == y2:
        return "same loc"
    return direction

def translate_same_locs(dir_list, best_solution, rotations):
    '''Given a direction list, translate tiles that occur multiple times
    to the correct moves (involving a smash)'''
    new_dir_list = []
    counter = 0
    smash_count = 0
    first_tile = True
    # Count the amount of 'same locs', then call get_moves() to translate
    for i, direction in enumerate(dir_list):
        if direction == "same loc":
            counter+=1
            if i == len(dir_list)-1:
                moves = get_moves(counter, first_tile, rotations)
                new_dir_list.extend(moves)          
        else:
            moves = get_moves(counter, first_tile, rotations)
            new_dir_list.extend(moves)
            new_dir_list.append(direction)
            counter = 0
            first_tile = False
    return new_dir_list

def get_moves(counter, first_tile, rotations):
    ''' Given a counter and the rotations, return the correct sequence of 
    moves''' 
    moves = []
    if counter == 1:
        moves = ["smash"]
        del rotations[0]
    elif counter == 2:
        if first_tile:
            moves = [rotations[0], "smash"]
            del rotations[0]
        else:
            moves = [rotations[0], "smash"]
            del rotations[0]
    elif counter == 3:
        moves = ["smash", rotations[0], "smash"]
        del rotations[0]
    return moves

