from tkinter import *
import random

def init(data):
    data.scrollX = 0
    data.scrollMargin = 50
    data.playerX = data.scrollMargin
    data.playerY = 0
    data.playerWidth = 10
    data.playerHeight = 20
    data.doodles = 5
    data.doodlePoints = [0] * data.doodles
    data.doodleWidth = 20
    data.doodleHeight = 40
    data.listOfDoodleXSpacing = [45, 90, 135, 30, 60]
    data.listOfDoodleYSpacing = [10, -10, -20, 15, -25]
    data.doodleXSpacing = None
    data.doodleYSpacing = None
    data.currentDoodleCollect = -1
    data.listOfDoodles = list(range(data.doodles))


def getPlayerBounds(data):
    (x0, y1) = (data.playerX, data.height/2 - data.playerY)
    (x1, y0) = (x0 + data.playerWidth, y1 - data.playerHeight)
    return (x0, y0, x1, y1)

def getDoodleBounds(doodle, data):
    (x0, y1) = ((1 + doodle) * data.doodleXSpacing, 
                data.height/2 + (1 + doodle) * data.doodleYSpacing)
    (x1, y0) = (x0 + data.doodleWidth, y1 - data.doodleHeight)
    data.listOfDoodles.append((x0, y0, x1, y1))
    return (x0, y0, x1, y1)

def getDoodleCollect(data):
    playerBounds = getPlayerBounds(data)
    for doodle in range(data.doodles):
        data.doodleXSpacing = data.listOfDoodleXSpacing[doodle]
        data.doodleYSpacing = data.listOfDoodleYSpacing[doodle]
        doodleBounds = getDoodleBounds(doodle, data)
        if (boundsIntersect(playerBounds, doodleBounds) == True):
            return doodle
    return -1


def boundsIntersect(boundsA, boundsB):
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

def movePlayer(dx, dy, data):
    data.playerX += dx
    data.playerY += dy
    if (data.playerX < data.scrollX + data.scrollMargin):
        data.scrollX = data.playerX - data.scrollMargin
    if (data.playerX > data.scrollX + data.width - data.scrollMargin):
        data.scrollX = data.playerX - data.width + data.scrollMargin

    doodle = getDoodleCollect(data)
    if (doodle != data.currentDoodleCollect):
        data.currentDoodleCollect = doodle
        if (doodle >= 0):
            data.listOfDoodles.remove(doodle)

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if (event.keysym == "Left"): movePlayer(-5, 0, data)
    elif (event.keysym == "Right"): movePlayer(+5, 0, data)
    elif (event.keysym == "Up"): movePlayer(0, +5, data)
    elif (event.keysym == "Down"): movePlayer(0, -5, data)

def timerFired(data):
    pass

def redrawAll(canvas, data):
    lineY = data.height/2
    lineHeight = 5

    sx = data.scrollX
    for doodle in data.listOfDoodles:
        data.doodleXSpacing = data.listOfDoodleXSpacing[int(doodle)]
        data.doodleYSpacing = data.listOfDoodleYSpacing[int(doodle)]
        (x0, y0, x1, y1) = getDoodleBounds(doodle, data)
        fill = "orange" if (doodle == data.currentDoodleCollect) else "pink"
        canvas.create_rectangle(x0 - sx, y0, x1 - sx, y1, fill = fill)
        (cx, cy) = ((x0+x1)/2 - sx, (y0+y1)/2)
        canvas.create_text(cx, cy, text = str(data.doodlePoints[doodle]))
        cy = lineY + 5
        #canvas.create_text(cx, cy, text = str(doodle), anchor = N)
    
    (x0, y0, x1, y1) = getPlayerBounds(data)
    canvas.create_oval(x0 - sx, y0, x1 - sx, y1, fill = "grey")

    msg = "Use arrows to move, collect doodls to score"
    canvas.create_text(data.width/2, 20, text = msg)

####################################
# use the run function as-is
####################################

def run(width=400, height=400):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='tan', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 400)


