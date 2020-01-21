# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import random
import heapq
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    # initialization
    start = maze.getStart()
    end = maze.getObjectives()
    queue = [start]
    explored = []
    lineage = {}            #track which node explored which
    path = []
    goal = False
    temp = end[0]
    exp = 0
    # exceptions
    if (start == None or end == []):
        return [], 0

    # main loop
    while goal == False:

        curr = queue[0]         #hold front of queue then remove from queue
        queue.pop(0)

        if (curr not in explored):      #if it is not explored put it in explored
            explored.append(curr)
        else:                           #else we saw it already
            continue

        if (end[0][0] == curr[0] and end[0][1] == curr[1]):     #end check
            goal = True
            continue

        neigh = maze.getNeighbors(curr[0], curr[1])             #get neighbor LIST of TUPLES
        unvisited = []                                          #create unvisited list

        for i in range(len(neigh)):                             #if unvisited add to list
            if (neigh[i] not in explored):
                unvisited.append(neigh[i])
        exp += len(unvisited)
        queue.extend(unvisited)                                 #attach invisited to the queue

        for i in unvisited:                                     #link the children of curr to curr for backtracking
            lineage[i] = curr

    path.append(temp)                                           #add the end to the path
    while (temp != start):                                      #backtrack from end to get our path
        p = lineage[temp]
        path.append(p)
        temp = p
    #print (path)
    return path[::-1], exp                            #flip path so we start at start, # of states explored is the length of explored






def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    stack = []                          #stack for our nodes
    start = maze.getStart()
    stack.append(start)
    end = maze.getObjectives()
    explored = []
    lineage = {}
    goal = False
    path = []
    exp = 0
    # exceptions
    if (start == None or end == []):
        return [], 0

    # main loop
    while goal == False:
        current = stack[-1]             #depth first takes top of stack
        del stack[-1]                   #delete top of stack
        #print (current)
        if current in explored:         #if we have seen it ignore it
            continue

        explored.append(current)
        if current == end[0]:           #at the end?
            goal == True
            break

        neighbors = maze.getNeighbors(current[0], current[1])       #get neighbors

        for neighbor in neighbors:                                  #add unvisited neighbors to stack
            if neighbor not in explored:
                stack.append(neighbor)
                #print(neighbor)
                lineage[neighbor] = current                         #keep lineage for backtracking later
                exp += 1
    current = end[0]
    path.append(end[0])
    while (current != start):                                      #backtrack from end to get our path
        p = lineage[current]
        #print (p)
        path.append(p)
        current = p
    #print (path)
    return path[::-1], exp



def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    # initialization
    start = maze.getStart()
    end = maze.getObjectives()
    queue = [start]
    explored = []
    lineage = {}            #track which node explored which
    path = []
    goal = False
    temp = end[0]
    exp = 0

    # exceptions
    if (start == None or end == []):
        return [], 0

    # main loop
    while goal == False:

        curr = queue[0]         #hold front of queue then remove from queue
        queue.pop(0)

        if (curr not in explored):      #if it is not explored put it in explored
            explored.append(curr)
        else:                           #else we saw it already
            continue

        if (end[0][0] == curr[0] and end[0][1] == curr[1]):     #end check
            goal = True
            continue

        neigh = maze.getNeighbors(curr[0], curr[1])             #get neighbor LIST of TUPLES
        unvisited = []                                          #create unvisited list

        # Added Heuristic Portion for Greedy Search
        dict_test = {}

        for n in neigh :
            dict_test[n] = abs(n[0]- end[0][0]) + abs(n[1] - end[0][1])  # Storing Coordinates as Keys and Manhattan Distance as Values
        sorted_coord = sorted(dict_test, key = dict_test.get)                                       # Sorting from least to greatst
        #print(dict_test)
        #print(sorted_coord)
        for coord in sorted_coord :
            if( coord not in explored ) :                           #if unvisited add to list
                unvisited.append(coord)
        # End of Heuristic Implementation
        exp += len(unvisited)

        queue.extend(unvisited)                                 #attach invisited to the queue

        for i in unvisited:                                     #link the children of curr to curr for backtracking
            lineage[i] = curr

    path.append(temp)                                           #add the end to the path
    while (temp != start):                                      #backtrack from end to get our path
        p = lineage[temp]
        path.append(p)
        temp = p
    #print (path)
    return path[::-1], exp                            #flip path so we start at start, # of states explored is the length of explored




def astar(maze):
    # # TODO: Write your code here
    # # return path, num_states_explored

    start = maze.getStart()                 #get start
    end = maze.getObjectives()              #get multiple objectives
    frontier = []                           #min heap
    # heapq.heappush(frontier, (0, start))    #put start on heap with highest priority (smallest cost)
    came_from = {}                          #dictionary for parents and children
    cost_so_far = {}                        #cost accumulated
    came_from[start] = None                 #start has no parent
    cost_so_far[start] = 0                  #no cost from start
    path = []                               #path through maze
    end_temp = []                         #sort objectives
    counter = len(end)                      #how many objectives
    temp = start                            #initalize to start to calculate distance


    #1) Empty Dictionary after each objective
    #2) Need to still use cost/distance for decision making
    #3) Put final path into end of objective

    temp_node = start
    counter = 0
    while end != [] :                #for each objective
         distance = mandist(temp[0],temp[1],end[0][0],end[0][1])            #find manhattan distance from current location
         end_temp.append(end[0])                                            #append the node we are looking at
         temp_node = end[0]

         counter += 1
         for node in end:                                                   #for each remaining objective
             temp_distance = mandist(node[0],node[1],temp[0],temp[1])

             if temp_distance < distance and node not in end_temp :        #if we find a closer one
                 del end_temp[-1]
                 distance = temp_distance
                 temp_node = node
                 end_temp.append(node)                                          #set it in end_temp (closest to farthest)

         end.remove(temp_node)                                            #remove the one we added
         temp = temp_node                                                 #update temp

    temp = start
    end = list(end_temp)                                                          #end_temp will have objectives removed as we find them
    final_path = []
    path.append(temp)
    explored = []

    while end_temp != []:                       #while we have objectives
        came_from = {}
        cost_so_far = {}
        cost_so_far[start] = 0
        path = []
        heapq.heappush(frontier, (0, start))

        while frontier != []:                   #while stuff is on the frontier
            # print("Current Nodes in Frontier: ", frontier)
            current = heapq.heappop(frontier)   #take highest priority (smallest cost) off of heap

            # END CONDITIONS ###################################################
            if current[1] == end_temp[0]:        #if we find an objective
                # print("found" , end_temp[0])
                end_temp.remove(end_temp[0])     #remove from list
                frontier = []
                temp = current[1]

                # Bookeeping Path Taken from Objective to Objective
                while temp != start :
                    path.append( came_from[temp][1] )
                    temp = came_from[temp][1]

                # Update new Starting point at new objective and add path to the final path
                start = current[1]
                path.reverse()
                final_path.extend(path)


                # Clear all the other path cost in dict and include only one taken in path
                nodes = []

                for key in cost_so_far :
                    nodes.append(key)

                for key in nodes :
                    if key not in final_path :
                        cost_so_far.pop(key)

                break ;
            ####################################################################

            neigh = maze.getNeighbors(current[1][0], current[1][1])         #get neighbors of current node

            for neighbor in neigh:                                          #iterate through neighbors
                new_cost = cost_so_far[current[1]] + 1                      #calculate the cost of each
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:         #if neighbor isn't in cost dict, ad it. OR if the cost is less, replace it
                    cost_so_far[neighbor] = new_cost                                        #add cost to dict
                    priority = new_cost + mandist(current[1][0], current[1][1], neighbor[0], neighbor[1])           #this is f_n, h_n is manhattan and g_n is "new cost"
                    heapq.heappush(frontier, (priority, neighbor))                                                  #put onto min heap
                    came_from[neighbor] = current                                                                   #update lineage

                    if neighbor not in explored :
                        explored.append(neighbor)


    temp = end[-1]                                              #start from our last objective
    final_path.append(temp)                                           #add the end to the path

    return final_path, len(explored)                            #STILL NEED TO RETURN # OF EXPLORED NODES


def mandist(r1, c1, r2, c2):
    return (abs(r1 - r2) + abs(c1 - c2))
