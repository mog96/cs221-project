grid = []
borderWidth = 5
pointSpacing = 5

def setup():
    size(1180, 680)
    background(255)
    grid = makeGrid()
    drawGrid()

def draw():
    pass

def drawGrid():
    print grid
    for row in grid:
        for p in row:
            print p
            fill(0)
            ellipse(p.x, p.y, 2, 2)

# Place one point every 5 pixels.
def makeGrid():
    newGrid = []
    yIndex = 0
    for y in range(borderWidth, height - borderWidth, pointSpacing):
        newGrid.append([])
        for x in range(borderWidth, width - borderWidth, pointSpacing):
            newGrid[yIndex].append(point(x, y))
        yIndex += 1
    return newGrid