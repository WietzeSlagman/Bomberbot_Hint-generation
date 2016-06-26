'''
    File: main.py
    Authors: Joeri Bes, Haischel Dabian, Jim Buissink, Sebastiaan Joustra and
        Wietze Slagman
    Date: 16/06/2016
    Python version: 3.x
    Created for the Bomberbot coorporation
---------------------------------------------
    File description:
    This file contains the main file in order to run the program. 
'''
import parse_json
import parse_output
import objects
import hint_generation
import copy
import astar
import time
import sys
import brute_force

def main():
    # Selecting level
    filename = "Json/mission" + sys.argv[1] + "-level" + sys.argv[2] + ".json"

    # Initializing variables
    start_time = time.time()
    tile_list = []
    tiles = parse_json.get_tiles(filename)
    dimension = parse_json.get_dimensions(filename)
    has_hammer = parse_json.has_hammer(filename)
    start_location = parse_json.get_pos_player(filename)
    direction = parse_json.get_dir_player(filename)
    best_solution = parse_json.get_best_solutions(filename)

    # Searching for a demo for the level
    demo = parse_json.get_demo(sys.argv[1],sys.argv[2])
    if demo is not None:
        moves = demo[0]
        goals_collected =  demo[1]
    else:
        print("No demo found")
        moves = []
        goals_collected = []
    
    # Creating the tile grid
    rows = tiles.split(';')
    for y in range(len(rows)):
        row = rows[y].split(',')
        for x in range(len(row)):
            tile_list.append(create_tile(row[x], x, y))

    # Ceating the goal list
    goal_list = create_goal_list(tile_list)
    
    # Receiving the start location on the tiles 
    start_tile = get_tile(tile_list, start_location[0], start_location[1], \
        dimension[1], dimension[0])

    # Calling the brute force algorithm
    b = brute_force.Brute_force(dimension[1], dimension[0], tile_list, \
        goal_list, best_solution, start_tile, has_hammer, direction)
    best_path, rotations, permutations = b.solve()

    # Displaying the answer in commando's 
    output = parse_output.parse(best_path, start_tile, best_solution, \
        rotations)

    print("--- Level information ---")
    print("Starting location: (" + str(start_location[0]) + ", " + \
        str(start_location[1]) + ")")
    print("Starting direction:", direction)

    # Displaying the grid for the users
    display_grid(start_location, dimension, tiles)

    print("\n--- Path info ---")
    print ('Path found:', len(best_path), 'moves. |  ' 'Best solution:', \
        best_solution,' moves. | Permutation used', permutations)
    print("Best path: ", ', '.join(output))
    print("User path: ",', '.join(moves))

    # Creating hints for the user if necessary
    print("\n--- Hint generated ---")
    hint = hint_generation.Hint_generation(moves, output, goals_collected, \
        goal_list, permutations)
    hint.process()

    print("\n--- Run time: ---")
    print("%s seconds" % (time.time() - start_time))


def create_goal_list(tile_list):
    '''This function loops through every tile and adds every star, 
    ruby or hammer it encounters to the goal list.  
    '''
    goal_list = []
    for tile in tile_list:
        if tile.get_object_name() == "Star" or tile.get_object_name() == "Ruby" \
            or tile.get_object_name() == "Hammer":
            goal_list.append((tile, tile.obj))
    return goal_list


def get_tile(tile_list, x, y, height, width):
    '''When given coordinates, this function calculates which tile
    matches from the tile list.
    '''
    return tile_list[y * width + x]

def create_tile(value, x, y):
    '''This function creates the tiles by the given values from the json 
    file.
    ''' 
    slidable = False
    abyss = False
    tile = None
    obj = None

    if value[0] == "b":
        slidable = True
    if value[0] == ".":
        obj = objects.Brick(False)
    else:
        if len(value) == 2:
            if value[1] == "4":
                obj = objects.Star()
            elif value[1] == "3":
                obj = objects.Ruby()
            elif value[1] == "1":
                obj = objects.Brick(True)
            elif value[1] == "6":
                obj = objects.Hammer()
            else:
                obj = objects.Brick(False)
    tile = objects.Tile(slidable, obj, x, y)
    return tile

def display_grid(start_location, dimension, tiles):
    grid = prep_grid(start_location, dimension, tiles)
    printgrid(grid)

def prep_grid(start_location, dimension, tiles):
    '''This function displays the grid for the user.'''
    grid = [([None]*dimension[0]) for i in range(dimension[1])]

    rows = tiles.split(';')
    for y in range(len(rows)):
        row = rows[y].split(',')
        for x in range(len(row)):
            grid[y][x] = create_tile(row[x], x, y)


    for i in range(len(grid)):
        for j in range(len(grid[i])):
            tile = grid[i][j]       
            if tile.has_object():
                if tile.get_object_name() == "Brick":
                    if tile.obj.destroyable == True:
                        grid[i][j] = "D"
                    else:
                        grid[i][j] = "X"
                elif tile.get_object_name() == "Star":
                    grid[i][j] = "S"
                elif tile.get_object_name() == "Hammer":
                    grid[i][j] = "H"
                elif tile.get_object_name() == "Ruby":
                    grid[i][j] = "R"
                else:
                    grid[i][j] = "?"
            else:
                grid[i][j] = " "

    grid[start_location[1]][start_location[0]] = "B"
    return grid

def printgrid(grid):
    '''This function prints the grid to terminal'''
    first=True
    for i in range(len(grid)):
        middle = ""
        bottom = "  "
        firstline = "  "
        top = "  "
        x_axis = "  "
        count_x_axis = 0
        for j in grid[i]:
            top += "|     "
            middle = middle + "  |  " + j
            bottom += "|_____"
            firstline += "______"
            x_axis += "   "+str(count_x_axis)+"  "
            count_x_axis += 1
        if first:
            print(" "+firstline+"_")
            first = False
        else:   
            print(" "+bottom+"|")
        print(" "+ top +"|")    
        print(str(i) + middle + "  |")
    print(" " + bottom + "|")
    print (" "+x_axis)


if __name__ == "__main__":
    main()