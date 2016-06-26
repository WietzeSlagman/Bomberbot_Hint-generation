'''
    File: astar.py
    Authors: Joeri Bes, Haischel Dabian, Jim Buissink, Sebastiaan Joustra and
        Wietze Slagman
    Date: 16/06/2016
    Python version: 3.x
    Created for the Bomberbot coorporation
---------------------------------------------
    File description:
    This file contains the implementation of the A* algorithm. The A* algorithm
    is a search algorithm to find the shortest path towards the goal. This 
    implementation is based on the Bomberbot puzzles.  

'''

import math

class AStar(object):
    def __init__(self, grid_height, grid_width, tiles, start, end, has_hammer, \
        direction):
        self.opened = []
        self.closed = set()
        self.tiles = tiles
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.start = start
        self.end = end
        self.path_length = 0
        self.rotations = []
        self.has_hammer = has_hammer
        self.direction = direction

    def get_heuristic(self, tile):
        """Calculates the heuristic for the tiles. The heuristic is 
        a combination of euclidean distance and the reversed breaking
        ties method. The reversed breaking ties method prioritizes vertices 
        closer to the goal instead of close to the starting point.
        """ 

        # Euclidean distance
        dx = abs(tile.x_coord - self.end.x_coord)
        dy = abs(tile.y_coord - self.end.y_coord)
        heuristic = 10* math.sqrt(dx*dx + dy*dy) 

        # Reversed breaking ties method 
        dx1 = tile.x_coord - self.end.x_coord
        dy1 = tile.y_coord - self.end.y_coord
        dx2 = self.start.x_coord - self.end.x_coord
        dy2 = self.start.y_coord - self.end.y_coord
        cross = abs(dx1*dx2 - dx2*dy1)
        heuristic -= cross*2.5
        return heuristic

    def get_tile(self, x, y):
        '''When given coordinates, this function calculates which tile matches 
        from the tile list.
        '''
        return self.tiles[y * self.grid_width + x]


    def get_adjacent_tiles(self, tile):
        '''Given a tile, return all adjacent tiles.'''
        tiles = []
        if tile.x_coord < self.grid_width-1:
            tiles.append(self.get_tile(tile.x_coord+1, tile.y_coord))
        if tile.y_coord > 0:
            tiles.append(self.get_tile(tile.x_coord, tile.y_coord-1))
        if tile.x_coord > 0:
            tiles.append(self.get_tile(tile.x_coord-1, tile.y_coord))
        if tile.y_coord < self.grid_height-1:
            tiles.append(self.get_tile(tile.x_coord, tile.y_coord+1))
        return tiles

    def get_path(self):
        '''Starting from the end tile, find parents till the start tile is
        reached. Returns the best path.
        '''
        path_list = []
        tile = self.end
        path_length = 0
        path_list.append(tile)
        while tile.parent is not None:

            # Add copies of a move when a destroyable object is found
            if tile.has_object() and tile.obj.destroyable:
                if tile.obj.destroyed:
                    cost = tile.obj.destroy_cost
                    if tile.parent.obj is not None:
                        if tile.parent.get_object_name() == "Ruby":
                            tile.parent.obj.destroy_cost = 0
                    if cost != 0:
                        dr = self.get_direction(tile.parent.x_coord, \
                            tile.parent.y_coord, tile.x_coord, tile.y_coord)
                        self.rotations.append(dr)
                        for i in range(cost):
                            path_list.append(tile.parent)
                        path_length += cost
               
            tile = tile.parent
            path_list.append(tile)

        # Delete the first element in the list if it's a ruby, since the bot 
        # doesn't have to end on the ruby itself
        if path_list[0].get_object_name() == "Ruby":
            del path_list[0]

        # Find end direction
        if path_list != [] and path_list[0].parent is not None:
            self.direction = self.get_direction(path_list[0].parent.x_coord, \
                path_list[0].parent.y_coord, path_list[0].x_coord, \
                path_list[0].y_coord)

        self.path_length = str(len(path_list)-1)

        return path_list, self.direction, self.rotations

    def set_parent_tile(self, adj, tile, increment):
        '''Given a tile and its adjacent tile, adjust the f score and 
        add the current tile as parent to the adjacent tile 
        '''
        adj.g = tile.g + increment
        adj.h = self.get_heuristic(adj)
        adj.parent = tile
        adj.f = adj.h + adj.g

    def process(self):
        '''This is the main function of A* and is called to calculate and 
        return the best path.
        '''
        self.opened.append((self.start.f, self.start))
        while len(self.opened):

            # Opened list functions as a queue.
            self.opened = sorted(self.opened, key=lambda tup: tup[0])
            (f, tile) = self.opened[0]
            del self.opened[0]

            self.closed.add(tile)
            if tile is self.end:
                return self.get_path()
                
            adj_tiles = self.get_adjacent_tiles(tile)

            # Go through every adjacent tile and calculate the score
            for adj_tile in adj_tiles:
                obj = adj_tile.obj
                if adj_tile.is_walkable() and adj_tile not in self.closed:
                    self.check_in_opened(tile, adj_tile, 10, 0, False)            

                # Destroyable object found
                elif adj_tile.has_object() and not adj_tile.is_walkable() and \
                    obj.destroyable and adj_tile not in self.closed and \
                    self.has_hammer:

                    parent = tile.parent
                    # Find the direction of the bomberbot in relation to the
                    # next tile
                    if parent is not None:
                        bot_dir = self.get_direction(parent.x_coord, \
                            parent.y_coord, tile.x_coord, tile.y_coord)
                    else:
                        bot_dir = self.direction

                    next_dir = self.get_direction(tile.x_coord, tile.y_coord, \
                        adj_tile.x_coord, adj_tile.y_coord)

                    # Check if direction is the same, and apply correct cost
                    if bot_dir == next_dir:
                        self.check_in_opened(tile, adj_tile, 20, 1, True)
                    else:
                        self.check_in_opened(tile, adj_tile, 30, 2, True)
            
    def check_in_opened(self, tile, adj_tile, g_cost, destroy_cost, destroy):
        '''Check if tile is in opened list. Set parent tile and destroy brick
        or ruby if apllicable.
        '''
        if (adj_tile.f, adj_tile) in self.opened:
            if adj_tile.g > tile.g + g_cost:
                self.set_parent_tile(adj_tile, tile, g_cost)
        else:
            self.set_parent_tile(adj_tile, tile, g_cost)
            self.opened.append((adj_tile.f, adj_tile))
            if destroy:
                adj_tile.obj.destroy()
                adj_tile.obj.destroy_cost = destroy_cost

    def get_direction(self, x_prev, y_prev, x_curr, y_curr):
        ''' Given the coordinates of two tiles, return the relative 
        direction.
        '''
        direction = ""
        if x_curr > x_prev:
            direction = "right"
        if x_curr < x_prev:
            direction = "left"
        if y_curr > y_prev:
            direction = "down"
        if y_curr < y_prev:
            direction = "up"

        return direction