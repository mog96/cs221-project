###############################################################################

#               W A V Y             L I N E               A I

###############################################################################


class WavyLineProblem(util.SearchProblem):
    def __init__(self, width, height, startPoint):
        self.width = width
        self.height = height
        self.startPoint = startPoint  # Tuple representing initial (x, y)'
        self.lineLength = 0
        self.maxLineLength = 60

    # Staerting point and 2-D array of grid locations. Each point in the grid
    # will contian the coordinates of the next point in the line.
    def startState(self):
        return (self.startPoint, [[None] * self.width] * self.height, lineLength)

    def isEnd(self, state):
        _, _, lineLength = state
        return lineLength == self.maxLineLength

    def succAndCost(self, state):
        # TODO: fix VV
        currentPoint, distance = state
        newStates = []
        if distance + 1 <= self.maxLineLength:
            for point in self.surroundingPoints(currentPoint):
                #

            # TODO: Replace vv

            for endIndex in range(state[1] + 1, len(self.query) + 1): # range() end index is exclusive
                action = self.query[state[1] : endIndex]
                newStates.append((action, (state[1], endIndex), self.unigramCost(action)))

        return newStates

    # Returns the set of valid points surrounding point.
    def surroundingPoints(self, point):
        #



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
