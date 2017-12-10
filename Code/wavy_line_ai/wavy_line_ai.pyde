###############################################################################

#               W A V Y             L I N E               A I

###############################################################################

import random

class WavyLineProblem(util.SearchProblem):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1

    def __init__(self, width, height, startPoint):
        assert(width > 0 and height > 0)
        self.width = width
        self.height = height
        x, y = startPoint
        assert(x >= 0 and x < width)
        assert(y >= 0 and y < height)
        self.startPoint = startPoint  # (x, y) tuple
        self.changeDirectionProb = .314
        self.maxLineLength = 60
        random.seed(42)                        # TODO: Remove from prod

    # Returns the start state:
    #   - Starting point as an (x, y) tuple
    #   - 2-D array of grid locations organized as a list of rows
    #   - Current direction of motion: clockwise or counterclockwise
    # Each visited point in the grid stores the coordinates of the next point
    # in the line being drawn. Unvisited points in the grid are therefore set
    # to 'None'.
    # Development version contains line length state parameter as well.
    def startState(self):
        startingGrid = self.startPoint, [[None] * self.width] * self.height
        startingDirection = random.choice([CLOCKWISE, COUNTERCLOCKWISE])
        startingLineLength = 0
        return (startingGrid, self.startPoint, self.startingDirection, \
            startingLineLength)

    # Returns whether |state| is an end state or not: True if all points
    # surrounding current point have been visited.
    # Development version checks whether line length has exceeded max.
    def isEnd(self, state):
        _, _, lineLength = state
        return lineLength == self.maxLineLength or \
            self.surroundingPoints(state) is None

    # Returns a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|. Actions are:
    #   - Move in the current direction of motion (clockwise/counterclockwise)
    #   - Move in the other direction
    # as the current grid permits. Any step taken that can be considered as
    # continuing in the current direction is considered as such. So, for
    # example, a step taken to get around a visited point, if necessary to
    # continue in the current direciton, is considered the same as the current
    # direction. Conversely, a step taken that is not necessary to continue in
    # the current direction is considered to be the other direction of motion.
    # New state is comprised of:
    #   - New current point selected from unvisited points surrounding
    #     |state|'s current point
    #   - New grid, updated from the previous grid such that |state|'s current
    #     point is populated with |newState|'s current point
    #   - New direction of motion, if changed; else same as before.
    # Cost is a random number in the range [0.0, 1.0).
    # Development version stores incremented line length in |newState| as well.
    def succAndCost(self, state):
        newStates = []
        _, _, currentDirection, lineLength = state
        if lineLength + 1 <= self.maxLineLength:
            if self.shouldChangeDirection():
                # Only return states that represent change in direction
            else:
                # Only return states that represent continuing in same
                # direction
            for point in self.unvisitedSurroundingPoints(state):


                # TODO: START HERE
                #       Need to figure out how to apply probability to cost
                #       how to negotiate surrounding points
                #       vs. action of 'Clockwise' or 'Counterclockwise'


                # action = 'Clockwise' or 'Counterclockwise'
                # cost = random.random()
                # newStates.append((action, (newGrid, nextPoint, lineLength + 1), cost))

        return newStates

    # Returns a list of the unvisited points in |state|'s grid surrounding
    # |state|'s current point.
    def unvisitedSurroundingPoints(self, state):
        points = []
        grid, currentPoint, _, _ = state
        currentX, currentY = currentPoint
        xMin, xMax = max(0, currentX - 1), min(self.width - 1, currentX + 1)
        yMin, yMax = max(0, currentY - 1), min(self.height - 1, currentY + 1)
        for x in range(xMin, xMax + 1):       # range() end index is exclusive
            for y in range(yMin, yMax + 1):
                if grid[y][x] is not None and (x, y) != currentPoint:
                    points.append((x, y))
        return points

    def shouldChangeDirection(self):
        return random.random() <= self.changeDirectionProb



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
