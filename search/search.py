# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import game

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        # util.raiseNotDefined()
        cost = 0
        for path in actions:
            cost += path[2]
        return cost

search_problem = SearchProblem()
def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    open = util.Stack()
    #create a open Stack to store the node/path
    path = []
    #create a empty node
    path.append((problem.getStartState(), game.Directions.STOP, 0))
    #Add a start state to this node to match the outcome of the successor class
    open.push(path)
    ans = []
    while not open.isEmpty():
        n = open.pop()
        #if there is an element in the open stack, pop it.
        end_state = n[-1];
        #so pop the last state of the list
        if(problem.isGoalState(end_state[0])):
            #check if the end state is our goal State, if it is then we are finished
            for seq in n[1:]:
                ans.append(seq[1])
            #return the Goal Path
            return ans
        else:
            #otherwise we need to modify our open stack
            for succ in problem.getSuccessors(end_state[0]):
                path_check = True
                for node in n:
                    if succ[0] in node:
                        path_check = False
                #path checking only checks if the state is already in the current path node in open
                if path_check:
                    my_path = n + [succ]
                    open.push(my_path)
    return ans

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    open = util.Queue()
    seen = {}
    path = []
    path.append((problem.getStartState(), game.Directions.STOP, 0))
    seen[problem.getStartState()] = 0
    open.push(path)
    ans = []
    while not open.isEmpty():
        n = open.pop()
        #if there is an element in the open stack, pop it.
        end_state = n[-1];
        #so pop the last state of the list
        curr_pos = end_state[0]
        if end_state[2] <= seen[curr_pos]:
            if(problem.isGoalState(curr_pos)):
                #check if the end state is our goal State, if it is then we are finished
                for seq in n[1:]:
                    ans.append(seq[1])
                return ans
            else:
                #otherwise we need to modify our open stack
                for succ in problem.getSuccessors(curr_pos):
                    #for s in problem.getSuccessors(problem.getStartState()):
                        #i need to change the cost in some way
                    my_path = n + [succ]
                    # print "The cost of this path is:", cost(tmp)
                    if succ[0] not in seen.keys() or search_problem.getCostOfActions(my_path) < seen[succ[0]]:
                    #cycle checking: so if it is in seen means it already been checked ignore it
                    #if it is not in seen then we should add it to open
                        open.push(my_path)
                        seen[succ[0]] = search_problem.getCostOfActions(my_path)
    return ans

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    open = util.PriorityQueue()
    path = []
    path.append((problem.getStartState(), game.Directions.STOP, 0))
    open.push(path, 0) 
    seen = {}
    seen[problem.getStartState()] = 0
    ans = []
    while not open.isEmpty():
        n = open.pop()
        curr_pos = n[-1][0]
        if search_problem.getCostOfActions(n) <= seen[curr_pos]:
            if problem.isGoalState(curr_pos):
                for seq in n[1:]:
                    ans.append(seq[1])
                return ans
            for succ in problem.getSuccessors(curr_pos):
                my_path = n + [succ]
                if not succ[0] in seen.keys() or search_problem.getCostOfActions(my_path) < seen[succ[0]]: 
                    open.push(my_path, search_problem.getCostOfActions(my_path))
                    seen[succ[0]] = search_problem.getCostOfActions(my_path)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # print(""
    # copy paste bfs then modify it using heurstics and f value f(n) = g(n) + h(n)
    open = util.PriorityQueue()
    path = []
    path.append((problem.getStartState(), game.Directions.STOP, 0))
    open.update(path, heuristic(problem.getStartState(),problem))
    seen = {}
    seen[problem.getStartState()] = 0
    ans = []
    while not open.isEmpty():
        n = open.pop()
        curr_pos = n[-1][0]
        if search_problem.getCostOfActions(n) <= seen[curr_pos]:
            if problem.isGoalState(curr_pos):
                for seq in n[1:]:
                    ans.append(seq[1])
                return ans
            for succ in problem.getSuccessors(curr_pos):
                my_path = n + [succ]
                my_fvalue = search_problem.getCostOfActions(my_path) + heuristic(succ[0], problem)
                if not succ[0] in seen.keys() or search_problem.getCostOfActions(my_path) < seen[succ[0]]: 
                    open.update(my_path, my_fvalue)
                    seen[succ[0]] = search_problem.getCostOfActions(my_path)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
