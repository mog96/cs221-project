###############################################################################

#               W A V Y             L I N E               A I

###############################################################################

import random

class WavyLineProblem(util.SearchProblem):
    def __init__(self, width, height, startPoint):
        assert(width > 0 and height > 0)
        x, y = startPoint
        assert(x >= 0 and x < width)
        assert(y >= 0 and y < height)
        self.width = width
        self.height = height
        self.startPoint = startPoint  # (x, y) tuple
        self.maxLineLength = 60

    # Returns the start state: Starting point as an (x, y) tuple and a 2-D
    # array of grid locations organized as a list of rows. Each visited point
    # in the grid stores the coordinates of the next point in the line being
    # drawn. Unvisited points are therefore set to 'None'.
    # Development version contains line length state parameter as well.
    def startState(self):
        startingGrid = self.startPoint, [[None] * self.width] * self.height
        startingLineLength = 0
        return (startingGrid, self.startPoint, startingLineLength)

    # Returns whether |state| is an end state or not: True if all points
    # surrounding current point have been visited.
    # Development version checks whether line length has exceeded max.
    def isEnd(self, state):
        _, _, lineLength = state
        return lineLength == self.maxLineLength or \
            self.surroundingPoints(state) is None

    # Returns a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|. |newState| contains a new current point and a new
    # grid, updated from the previous grid such that |state|'s current point is
    # populated with |newState|'s current point. Cost is a random number in the
    # range [0.0, 1.0).
    # Development version stores incremented line length in |newState| as well.
    def succAndCost(self, state):
        newStates = []
        _, _, lineLength = state
        if lineLength + 1 <= self.maxLineLength:
            for point in self.surroundingPoints(currentPoint):
                random.seed(42)                                # TODO: Remove


                # TODO: START HERE
                #       Need to figure out how to negotiate surrounding points
                #       vs. action of 'Clockwise' or 'Counterclockwise'


                # action = 'Clockwise' or 'Counterclockwise'
                # cost = random.random()
                # newStates.append((action, (newGrid, nextPoint, lineLength + 1), cost))

        return newStates

    # Returns a list of the unoccupied points in |state|'s grid surrounding
    # |state|'s current point.
    def surroundingPoints(self, state):
        points = []
        grid, currentPoint, _ = state
        currentX, currentY = currentPoint
        xMin, xMax = max(0, currentX - 1), min(self.width - 1, currentX + 1)
        yMin, yMax = max(0, currentY - 1), min(self.height - 1, currentY + 1)
        for x in range(xMin, xMax + 1):       # range() end index is exclusive
            for y in range(yMin, yMax + 1):
                if grid[y][x] is not None and (x, y) != currentPoint:
                    points.append((x, y))
        return points



###############################################################################
# Graphical Display

# Border will be at least this wide. May be slightly larger in order to center
# grid in frame given pointSpacing.
minBorderWidth = 10
pointSpacing = 10

grid = []

def setup():
    size(1180, 680)
    background(255)    
    global grid
    grid = makeGrid()
    
    print "GRID", grid
    print""
    
    drawGrid()
    drawLine()
    # frameRate(30)
    
    # TODO: Instantiate wavy line problem

def draw():
    # TODO: Draw line in red.
    # TODO: Setup state, etc. for search problem
    pass

def drawGrid():
    # print "GRID", grid
    for row in grid:
        for p in row:
            fill(0)
            ellipse(p.x, p.y, 2, 2)

# Place one point every 5 pixels.
def makeGrid():
    newGrid = []
    yBorderOffset = ((height - 2 * minBorderWidth) % pointSpacing) / 2
    print height
    xBorderOffset = ((width - 2 * minBorderWidth) % pointSpacing) / 2
    yIndex = 0
    for y in range(minBorderWidth + yBorderOffset, height - minBorderWidth, \
                       pointSpacing):
        newGrid.append([])
        for x in range(minBorderWidth + xBorderOffset, \
                           width - minBorderWidth, pointSpacing):
            newGrid[yIndex].append(Point(x, y))
        yIndex += 1
    return newGrid

def drawLine():
    firstPoint = grid[0][0]
    secondPoint = grid[0][1]
    stroke(255, 0, 0)
    curve(firstPoint.x, firstPoint.y, firstPoint.x, firstPoint.y, \
          secondPoint.x, secondPoint.y, secondPoint.x, secondPoint.y)
