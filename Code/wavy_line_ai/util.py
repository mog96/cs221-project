import heapq, collections, re, sys, time, os, random

###############################################################################
# Abstract interfaces for search problems and search algorithms.

class SearchProblem:
    # Return the start state.
    def startState(self): raise NotImplementedError("Override me")

    # Return whether |state| is an end state or not.
    def isEnd(self, state): raise NotImplementedError("Override me")

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state): raise NotImplementedError("Override me")

class SearchAlgorithm:
    # First, call solve on the desired SearchProblem |problem|.
    # Then it should set two things:
    # - self.actions: list of actions that takes one from the start state to an end
    #                 state; if no action sequence exists, set it to None.
    # - self.totalCost: the sum of the costs along the path or None if no valid
    #                   action sequence exists.
    def solve(self, problem): raise NotImplementedError("Override me")

###############################################################################
# Depth-first search with iterative deepening (DFS-ID).

class DepthFirstSearchIterativeDeepening(SearchAlgorithm):
    def __init__(self, verbose=0):
        self.verbose = verbose
        self.maxDepth = 10

    def solve(self, problem):
        # If a path exists, set |actions| and |totalCost| accordingly.
        # Otherwise, leave them as None.
        self.actions = []
        self.totalCost = 0
        self.numStatesExplored = 0

        self.problem = problem
        self.endState = problem.startState()

        while True:
            self.bestIntermSoln = None
            recurse([], self.endState, 0, 0)
            if self.bestIntermSoln is not None:
                newActions, newEndState, cost, depth = self.bestIntermSoln
                self.actions += newActions
                self.totalCost += cost
                self.numStatesExplored += depth
                self.endState = newEndState

        if self.numStatesExplored == 0:
            self.noPathFound()
        else:
            if self.verbose >= 1:
                print "numStatesExplored = %d" % self.numStatesExplored
                print "totalCost = %s" % self.totalCost
                print "actions = %s" % self.actions
                print "endState = %s" % self.endState

    def recurse(self, pastActions, state, pastCost, depth):
        if state is None:
            self.noPathFound()
            return

        self.numStatesExplored += 1
        if self.verbose >= 2:
            print "Exploring %s with pastCost %s" % (state, pastCost)
        
        # Check if we've reached an end state or our maximum depth; if so,
        # compare this solution to current best. Best intermediate solution is
        # updated if:
        #  - This solution has greater depth
        #  - This solution has equal depth but lower cost.
        if self.problem.isEnd(state) or depth == self.maxDepth:
            if self.verbose >= 3:
                print "Intermediate solution with depth = %s and state = %s" \
                    % depth, state
            _, _, bestCost, bestDepth = self.bestSolution
            if depth > bestDepth or pastCost < cost:
                if self.verbose >= 3:
                    print "Updating best intermediate solution"
                self.bestIntermSoln = (pastActions, state, pastCost, depth)
            return

        # Expand from |state| to new successor states,
        # updating the frontier with each newState.
        for action, newState, cost in problem.succAndCost(state):
            if self.verbose >= 3:
                print "  Action %s => %s with cost %s + %s" % \
                    (action, newState, pastCost, cost)
            actions = list(pastActions) + action
            self.recurse(actions, newState, pastCost + cost, depth + 1)

    def noPathFound(self):
        if self.verbose >= 1:
            print "No path found"
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0






###############################################################################
# Uniform cost search algorithm (Dijkstra's algorithm).

class UniformCostSearch(SearchAlgorithm):
    def __init__(self, verbose=0):
        self.verbose = verbose

    def solve(self, problem):
        # If a path exists, set |actions| and |totalCost| accordingly.
        # Otherwise, leave them as None.
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0

        # Initialize data structures
        frontier = PriorityQueue()  # Explored states are maintained by the frontier.
        backpointers = {}  # map state to (action, previous state)

        # Add the start state
        startState = problem.startState()
        frontier.update(startState, 0)

        while True:
            # Remove the state from the queue with the lowest pastCost
            # (priority).
            state, pastCost = frontier.removeMin()
            if state == None: break
            self.numStatesExplored += 1
            if self.verbose >= 2:
                print "Exploring %s with pastCost %s" % (state, pastCost)

            # Check if we've reached an end state; if so, extract solution.
            if problem.isEnd(state):
                self.actions = []
                while state != startState:
                    action, prevState = backpointers[state]
                    self.actions.append(action)
                    state = prevState
                self.actions.reverse()
                self.totalCost = pastCost
                if self.verbose >= 1:
                    print "numStatesExplored = %d" % self.numStatesExplored
                    print "totalCost = %s" % self.totalCost
                    print "actions = %s" % self.actions
                return

            # Expand from |state| to new successor states,
            # updating the frontier with each newState.
            for action, newState, cost in problem.succAndCost(state):
                if self.verbose >= 3:
                    print "  Action %s => %s with cost %s + %s" % (action, newState, pastCost, cost)
                if frontier.update(newState, pastCost + cost):
                    # Found better way to go to |newState|, update backpointer.
                    backpointers[newState] = (action, state)
        if self.verbose >= 1:
            print "No path found"

# Data structure for supporting uniform cost search.
class PriorityQueue:
    def  __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    # Insert |state| into the heap with priority |newPriority| if
    # |state| isn't in the heap or |newPriority| is smaller than the existing
    # priority.
    # Return whether the priority queue was updated.
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Returns (state with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE: continue  # Outdated priority, skip
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None) # Nothing left...