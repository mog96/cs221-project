###############################################################################
#
#               W A V Y             L I N E               A I
#
###############################################################################



class WavyLineProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return (0, 0)
        # END_YOUR_CODE
        
        
        
        
        
        # TODO: START HERE
        # Define search problem.
        
        
        
        

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        return state[1] == len(self.query)
        # END_YOUR_CODE

    def succAndCost(self, state): 
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        newStates = []
        if state[1] + 1 <= len(self.query):
            for endIndex in range(state[1] + 1, len(self.query) + 1): # range() end index is exclusive
                action = self.query[state[1] : endIndex]
                newStates.append((action, (state[1], endIndex), self.unigramCost(action)))
        return newStates


###############################################################################
# Graphical Display

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __repr__(self):
        return self.__str__()

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
