'''
    File: hint_generation.py
    Authors: Joeri Bes, Haischel Dabian, Jim Buissink, Sebastiaan Joustra and
        Wietze Slagman
    Date: 16/06/2016
    Python version: 3.x
    Created for the Bomberbot coorporation
---------------------------------------------
    File description:
    This file contains functions in order to generate a personal hints for 
    the users. 

'''

import sys

class Hint_generation(object):
    def __init__(self, user_moves, best_moves, goals_collected, goal_list, \
    		permutations):
        self.user_moves = user_moves
        self.best_moves = best_moves
        self.goals_collected = goals_collected
        self.goal_list = goal_list
        self.permutations = permutations

    def check_correctness(self):
        '''Compares the users input with the brute force solution.'''
        if len(self.goals_collected) == len(self.goal_list) and \
        	len(self.user_moves) <= len(self.best_moves):
            print("User found the Best path")
            return True
        elif len(self.goals_collected) == len(self.goal_list):
        	print("User path is complete, but it's not the shortest path")
        	return False
        print("User path is incomplete")
        return False

    def compare_commands(self):
        '''Analyzes the fault of the user when there's only one goal.'''
        for i in range(len(self.user_moves)):
            if i <= len(self.user_moves)-1 and i <= len(self.best_moves)-1 :
                if self.user_moves[i] != self.best_moves[i]:
                    print("Wrong move found at move", i+1)
                    print("User move is '" + str(self.user_moves[i]) + \
                    	"', but correct move is '" + str(self.best_moves[i])+"'.")
                    return          
        if len(self.user_moves) < len(self.best_moves) and len(self.user_moves) > 0:
            print("Current path is correct, but not yet done. Try looking at move '" + \
            	self.best_moves[len(self.user_moves)] + "' next")
        elif len(self.user_moves) == 0:
            print("No moves made, try looking at move '" + \
                self.best_moves[len(self.user_moves)] + "' next")
        else:
            print("Current path is correct, but you used too many moves at the end.")


    def hint_next_star(self):
        '''Analyses the fault of the user when there are multiple goals. 
        The hint is based on the next goal to collect.
        '''
        correct_goals = []
        for i in range(len(self.permutations)):
            if len(self.goals_collected) != 0:
                if i+1 > len(self.goals_collected) or i != self.goals_collected[i]:
                    sys.stdout.write("Goals ")
                    for j in correct_goals:
                        sys.stdout.write("(" + str(self.goal_list[j-1][0].x_coord) + \
                        	", " + str(self.goal_list[j-1][0].y_coord) + "), ")
                    print("are correctly collected.")
                    print("Try looking at tile (" + str(self.goal_list[i][0].x_coord) + \
                    	"," + str(self.goal_list[i][0].y_coord) + ") next")
                    break
                else:
                     correct_goals.append(self.permutations[i]+1)
            else:
                print("No stars collected yet. Try looking at tile (" + \
                	str(self.goal_list[self.permutations[0]][0].x_coord) + \
                	"," + str(self.goal_list[self.permutations[0]][0].y_coord) + ")")
                return

    def process(self):
        '''Checks whether the input of the user is correct. If not, 
        uses different functions based on how many goals there are.
        ''' 
        correct = self.check_correctness()
        if not correct:
            if len(self.goal_list) > 1:
                self.hint_next_star()
            else:
                self.compare_commands()
