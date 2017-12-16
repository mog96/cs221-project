###############################################################################

#               W A V Y             L I N E               A I

###############################################################################



import copy, math, random

# Abstract interfaces for search problems and search algorithms.

class SearchProblem:
    # Return the start state.
    def startState(self): raise NotImplementedError("Override me")

    # Return whether |state| is an end state or not.
    def isEnd(self, state): raise NotImplementedError("Override me")

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state): raise NotImplementedError("Override me")

    # Called by search algorithm to update the graphical display with the
    # current state.
    def updateDisplay(self, state): raise NotImplementedError("Override me")

    # Helpful in the event that the state is too large to be printed as-is.
    def stringForState(self, state): raise NotImplementedError("Override me")

class SearchAlgorithm:
    # First, call solve on the desired SearchProblem |problem|.
    # Then it should set two things:
    # - self.actions: list of actions that takes one from the start state to an
    #                 end state; if no action sequence exists, set it to None.
    # - self.totalCost: the sum of the costs along the path or None if no valid
    #                   action sequence exists.
    def solve(self, problem): raise NotImplementedError("Override me")



###############################################################################
# Wavy line search problem definition.

class WavyLineProblem(SearchProblem):
    def __init__(self, gridWidth, gridHeight, startPoint, updateDisplayFn):
        assert(gridWidth > 0 and gridHeight > 0)
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        x, y = startPoint
        assert(x >= 0 and x < gridWidth)
        assert(y >= 0 and y < gridHeight)
        self.startPoint = startPoint  # (x, y) tuple

        self.updateDisplayFn = updateDisplayFn

        # random.seed(42)

    # Returns the start state:
    #  - 2-D array of grid locations organized as a list of rows
    #  - Starting point as an (x, y) tuple
    # Each visited point in the grid stores the coordinates of the next point
    # in the line being drawn. Unvisited points in the grid are therefore set
    # to 'None'.
    def startState(self):
        startingGrid = [[None] * self.gridWidth] * self.gridHeight
        return (startingGrid, self.startPoint)

    # Returns whether |state| is an end state or not: True if all points
    # surrounding current point have been visited.
    def isEnd(self, state):
        return self.unvisitedSurroundingPoints(state) is None

    # Returns a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    #  - Action is a movement forward, left, or right.
    #  - New state is comprised of:m
    #    - New current point selected from unvisited points surrounding
    #     |state|'s current point
    #    - New grid, updated from the previous grid such that |state|'s current
    #     point is populated with |newState|'s current point
    #  - Cost is based on several deterministic factors, as well as some
    #    randomness.
    def succAndCost(self, state):
        succAndCosts = []
        currentGrid, currentPoint = state
        for newPoint in self.unvisitedSurroundingPoints(state):
            newGrid = [list(row) for row in currentGrid]
            x, y = currentPoint
            newGrid[y][x] = newPoint
            newState = (newGrid, newPoint)

            widthHeightAverage = (self.gridWidth + self.gridHeight) / 2
            randomFactor = random.random() * widthHeightAverage / 30
            surroundingPointsFactor = widthHeightAverage / 30
            if len(self.unvisitedSurroundingPoints(newState)) >= 3:
                surroundingPointsFactor *= 2.25
            cost = self.distanceFromStart(newPoint) * 0.5 \
                + self.distanceFromNearestCanvasEdge(newPoint) * 0.4 + \
                + randomFactor + surroundingPointsFactor

            succAndCosts.append(('advance', newState, cost))
        return succAndCosts

    # Returns a list of the unvisited points in |state|'s grid surrounding
    # |state|'s current point.
    def unvisitedSurroundingPoints(self, state):
        points = []
        grid, currentPoint = state
        currentX, currentY = currentPoint
        xMin = max(0, currentX - 1)
        xMax = min(self.gridWidth - 1, currentX + 1)
        yMin = max(0, currentY - 1)
        yMax = min(self.gridHeight - 1, currentY + 1)
        for x in range(xMin, xMax + 1):  # End index is exclusive in range()
            for y in range(yMin, yMax + 1):
                if grid[y][x] is None and (x, y) != currentPoint and \
                    (x == currentX or y == currentY):
                    points.append((x, y))
        return points

    def distanceFromStart(self, point):
        x1, y1 = self.startPoint
        x2, y2 = point
        return math.sqrt(abs(x2 - x1) ** 2 + abs(y2 - y1) ** 2)

    def distanceFromNearestCanvasEdge(self, point):
        x, y = point
        leftEdgeDist = x
        rightEdgeDist = (self.gridWidth - 1) - x
        topEdgeDist = y
        bottomEdgeDist = (self.gridHeight - 1) - x
        return min(leftEdgeDist, rightEdgeDist, topEdgeDist, bottomEdgeDist)

    # Called by search algorithm to update the graphical display with the
    # current state.
    def updateDisplay(self, state):
        grid, currentPoint = state
        self.updateDisplayFn(grid, currentPoint)

    def stringForState(self, state):
        _, currentPoint = state
        return currentPoint



###############################################################################
# Depth-first search with iterative deepening (DFS-ID).

# DFS-ID is implemented here such that it is depth-first to a fixed depth in
# order to find a segment of a path, and then repeated to construct a complete
# path. A path is considered complete when the start point for a new
# fixed-depth search is surrounded by points already visited by the path.
class DepthFirstSearchIterativeDeepening(SearchAlgorithm):
    def __init__(self, maxDepth, verbose=0):
        self.verbose = verbose
        self.maxDepth = maxDepth

    def solve(self, problem):
        # If a path exists, set |actions| and |totalCost| accordingly.
        # Otherwise, leave them as None.
        self.actions = []
        self.totalCost = 0
        self.numStatesExplored = 0

        self.problem = problem
        self.endState = problem.startState()

        iterCount = 0

        # Repeat DFS with a maximum depth until an end state is reached.
        while True:
            iterCount += 1
            if self.verbose >= 1:
                print "Iteration %s" % iterCount

            self.bestIntermSoln = None
            self.recurse([], self.endState, 0, 0)
            if self.bestIntermSoln is None:
                break
            newActions, newEndState, cost, depth = self.bestIntermSoln
            if len(newActions) == 0:
                break
            self.actions += newActions
            self.totalCost += cost
            self.numStatesExplored += depth
            self.endState = newEndState
            self.problem.updateDisplay(self.endState)

        if self.numStatesExplored == 0:
            self.noPathFound()
            return

        if self.verbose >= 1:
            print "numStatesExplored = %d" % self.numStatesExplored
            print "totalCost = %s" % self.totalCost
            print "actions = %s" % self.actions
            if self.verbose >= 4:
                print "endState = ",
                for item in self.endState:
                    print item,
                print ""
                print "Done!"

    def recurse(self, pastActions, state, pastCost, depth):
        if state is None:
            self.noPathFound()
            return

        self.numStatesExplored += 1
        if self.verbose >= 2:
            print "Exploring %s with pastCost %s" \
                % (self.problem.stringForState(state), pastCost)
        
        # Check if we've reached an end state or our maximum depth; if so,
        # compare this solution to current best. Best intermediate solution is
        # updated if:
        #  - This solution has greater depth
        #  - This solution has equal depth but lower cost.
        if self.problem.isEnd(state) or depth == self.maxDepth:
            if self.verbose >= 2:
                print "Intermediate solution with depth = %s and state = %s" \
                    % (depth, self.problem.stringForState(state))
            solution = (pastActions, state, pastCost, depth)
            if self.bestIntermSoln is not None:
                _, _, bestCost, bestDepth = self.bestIntermSoln
                if depth > bestDepth or (depth == bestDepth and pastCost \
                    < bestCost):
                    self.updateBestIntermSoln(solution)
            else:
                self.updateBestIntermSoln(solution)
            return

        # Expand from |state| to new successor states,
        # updating the frontier with each newState.
        for action, newState, cost in self.problem.succAndCost(state):
            if self.verbose >= 3:
                print "  Action %s => %s with cost %s + %s" % \
                    (action, self.problem.stringForState(newState), pastCost,
                        cost)
            actions = list(pastActions) + [action]
            self.recurse(actions, newState, pastCost + cost, depth + 1)

    def updateBestIntermSoln(self, newBest):
        if self.verbose >= 3:
            print "Updating best intermediate solution"
        self.bestIntermSoln = newBest

    def noPathFound(self):
        if self.verbose >= 1:
            print "No path found"
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0



###############################################################################
# Graphical display.

# Border will be at least this wide. May be slightly larger in order to center
# grid in frame given pointSpacing.
minBorderWidth = 10

pointSpacing = 10
# pointSpacing = 20
# pointSpacing = 40

grid = []

# startPoint = (0, 0)
# startPoint = (25, 15)
# startPoint = (30, 18)
startPoint = (50, 30)

segmentSearchDepth = 4
verbose = 1

# Sizes grid to the canvas, and then instantiates a WavyLineSearchProblem with
# the determined size.
def setup():
    size(1200, 700)
    # size(800, 600)
    background(0)    
    makeGrid()
    
    drawGridPoints()
    gridHeight = len(grid)
    if gridHeight == 0:
        raise Exception("Canvas not tall enough")
    gridWidth = len(grid[0])
    if gridWidth == 0:
        raise Exception("Canvas not wide enough")

    if verbose >= 1:
        print "Grid width = %s" % gridWidth
        print "Grid height = %s" % gridHeight

    dfsid = DepthFirstSearchIterativeDeepening(segmentSearchDepth, verbose)
    dfsid.solve(WavyLineProblem(gridWidth, gridHeight, startPoint, \
        updateDisplay))

    # drawLine()

def draw():
    pass

# Places one point every 5 pixels. Grid is represented internally as a 2-D
# array organized as a list of rows. Each grid location in this 2-D array
# contains the pixel coordinates of the grid point.
def makeGrid():
    global grid
    yMargin = minBorderWidth + gridBorderMargin(height)
    xMargin = minBorderWidth + gridBorderMargin(width)

    print "Y MARGIN", yMargin
    print "X MARGIN", xMargin

    colIndex = 0
    for y in range(yMargin, height - yMargin, pointSpacing):
        grid.append([])
        for x in range(xMargin, width - xMargin, pointSpacing):
            grid[colIndex].append((x, y))
        colIndex += 1

# Returns the amount that must be added to the minimum grid border in order
# to snugly fit the grid to the canvas size.
def gridBorderMargin(canvasWidthOrHeight):
    return ((canvasWidthOrHeight - 2 * minBorderWidth) % pointSpacing) / 2

# Draws grid points on canvas.
def drawGridPoints():
    # print "GRID", grid
    for row in grid:
        for x, y in row:
            fill(255, 255, 0)
            ellipse(x, y, 2, 2)

# Wipes canvas and draws the line stored in the grid parameter. Grid parameter
# is expected to be a 2-D array of grid locations organized as a list of rows,
# wherein each visited point in the grid stores the coordinates of the next
# point in the line being drawn. Unvisited points in the grid are therefore
# expected to be set to None.
def updateDisplay(currentGrid, currentEndPoint):
    currentPoint = startPoint
    while True:
        rowIndex, colIndex = currentPoint
        nextPoint = currentGrid[colIndex][rowIndex]
        if nextPoint is None:
            break
        drawLine(currentPoint, nextPoint)
        currentPoint = nextPoint

# Draws a line between the grid points denoted by startPoint and endPoint,
# which are (x, y) tuples.
def drawLine(startPoint, endPoint):
    startRow, startCol = startPoint
    endRow, endCol = endPoint
    startX, startY = grid[startCol][startRow]
    endX, endY = grid[endCol][endRow]
    stroke(255)
    curve(startX, startY, startX, startY, endX, endY, endX, endY)
