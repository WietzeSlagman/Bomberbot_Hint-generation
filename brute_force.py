'''
    File: brute_force.py
    Authors: Joeri Bes, Haischel Dabian, Jim Buissink, Sebastiaan Joustra and
        Wietze Slagman
    Date: 16/06/2016
    Python version: 3.x
    Created for the Bomberbot coorporation
---------------------------------------------
    File description:
    This file contains the functions in order to solve the puzzles via
    brute forcing the goals. 

'''

import astar
import copy
from itertools import permutations

class Brute_force:
    def __init__(self, grid_height, grid_width, tiles, goal_list, best_solution, \
        start, has_hammer, direction):
        self.goal_list = goal_list
        self.best_solution = best_solution
        self.start = start
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.tile_list = tiles
        self.has_hammer = has_hammer
        self.direction = direction
    
    def check_list(self, path_list):
        '''Checks whether all goals have been completed for a permutation.'''
        count = 0
        reached =[]
        for goal in self.goal_list:
            if goal[0].get_object_name()=="Ruby":
                if goal[0].obj.destroyed:
                    count+=1
            else:
                for tile in path_list:
                    if tile == goal[0] and tile not in reached:
                        count+=1
                        reached.append(tile)        
        if count == len(self.goal_list):
            return True
        return False

    def reset_parents(self, tile_list):
        '''Clearing the tile parents.''' 
        for tile in tile_list:
            tile.parent=None
        
    def reset_rubies(self, tile_list):
        '''Resetting the rubies.'''
        for tile in tile_list:
            if tile.has_object():
                if tile.get_object_name() == "Ruby":
                    tile.obj.destroyed = False

    def solve(self):
        '''Main process in order to solve brute force. The brute force solver 
        goes through every permutation of the goal list. For every element 
        in a permutation the A* (shortest path) will be calculated. When 
        the path length of a permutation is equal or lower to the best solution
        the function will be terminated and returned with the best path solution.
        '''

        # Initializing values
        best_path_length = 100
        best_path = []
        best_perm = ()
        rotations = []
        final_rotations = []

        # Going through every permutation of the goal list 
        for perm in permutations(range(len(self.goal_list))):
            current_step = self.start
            self.reset_rubies(self.tile_list)
            path_list = []
            rotations = []
            

            # Going through every element of the permutation
            for i in perm:
                self.reset_parents(self.tile_list)
                new_step = self.goal_list[i][0]
                
                # Calling the A* algorithm
                a = astar.AStar(self.grid_height, self.grid_width, \
                    self.tile_list, current_step, new_step, self.has_hammer, \
                    self.direction)
                astar_solution, self.direction, rot = a.process()
                rotations.extend(rot)
                # Delete the first step 
                if len(astar_solution) > 0:
                    del astar_solution[-1]

                # Reverse the path 
                if astar_solution is not None:
                    path_list.extend(reversed(astar_solution))
                else:
                    continue
                
                # Calculate current path length
                path_length = len(path_list)
                current_step = path_list[-1]                

                # Replace the path length if the current path length is lower.
                if (path_length == self.best_solution and self.check_list(path_list)):
                    best_path_length = path_length
                    best_perm = perm
                    best_path = path_list.copy()    
                    final_rotations = rotations.copy()

            #Terminate if best path length is shorter or equal than given best solution
            if best_path_length == self.best_solution:
                break

        final_rotations = list(reversed(final_rotations))
        return best_path, final_rotations, best_perm

    
if __name__ == "__main__":
    main()