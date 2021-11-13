from cmu_112_graphics_openCV import *
import random
import math
import cv2
import argparse

# fruit class
class fruit(object):
    def __init__(self, v, a):
        self.v = v
        self.t = 0
        self.a = a
        self.split = False
        self.x_after = None
        self.y_after = None

    # finds the x coordinate with respect to horizontal vectors
    def findX(self):
        return (self.v * math.cos(self.a) * self.t)

    # finds the  y coordinate with respect to vertical vectors
    def findY(self):
        if self.split == True:
            return self.y + 1
        return (self.v * math.sin(self.a) * self.t - 5 * self.t ** 2)

# subclasses of different fruits
# contains radius and color attributes
class apple(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r = 40
        self.color = "red"

class orange(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r= 50
        self.color = "orange"

class watermelon(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r = 60
        self.color = "green"

# appstarted
def appStarted(app):
    # app.image1 = app.loadImage('background.jpg')
    app.fruits = []
    app.timerDelay = 100
    app.x = None
    app.y = None
    app.r = 10
    app.time = 1
    app.cameraOpen = True
    app.lives = 1000
    app.gameOver = False

# mousepressed in substitute for cameraFired
"""
def mouseMoved(app, event):
    app.x = event.x
    app.y = event.y
    #if fruit is sliced, set coordinates for falling and split to True
    for fruit in app.fruits:
        if fruit.split == False and sliced(fruit.x, fruit.y, app.x, app.y, fruit.r):
            fruit.x_after = fruit.x
            fruit.y_after = fruit.y
            fruit.split = True
"""
# tracks the brightest pixel on the screen as tracker
# combined tacking code from https://www.pyimagesearch.com/2014/09/29/
# finding-brightest-spot-image-using-python-opencv/ with 112 graphics
def cameraFired(app):
    # flips screen to march direction of movement
    app.frame = cv2.flip(app.frame, 1)
    # converts image to grayscale
    gray = cv2.cvtColor(app.frame, cv2.COLOR_BGR2GRAY)
    # perform a naive attempt to find the (x, y) coordinates of
    # the area of the image with the largest intensity value
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    app.x = maxLoc[0]
    app.y = maxLoc[1]
    cv2.circle(app.frame, maxLoc, 5, (255, 0, 0), 2)
    # display the results of the naive attempt
    cv2.imshow("Naive", app.frame)
    # if fruit is sliced, set coordinates for falling and split to True
    for fruit in app.fruits:
      if fruit.split == False and sliced(fruit.x, fruit.y, app.x, app.y, fruit.r):
        fruit.x_after = fruit.x
        fruit.y_after = fruit.y
        fruit.split = True

# if r is pressed, game restarts
def keyPressed(app, event):
    if event.key == "r":
        appStarted(app)

# returns if fruit on screen is sliced
def sliced(x1, y1, x2, y2, r):
    return distance(x1,y1,x2,y2) <= r

# distance formula
def distance(x1,y1,x2,y2):
    return ((x2-x1) ** 2 + (y2- y1) ** 2) ** (1/2)

# timer fired
def timerFired(app):
    app.time += 1
    x = 100
    # randomly generates three fruits to be thrown from bottom of screen
    if app.time % 20 == 0:
        for i in range(3):
            #projectile motion variables
            n = random.randint(0,2)
            v = random.randint(70,80)
            a = random.randint(87,89)
            a = a * math.pi/180
            if n == 0:
                fruit = apple(v,a)
                app.fruits.append(fruit)
            elif n == 1:
                fruit = orange(v, a)
                app.fruits.append(fruit)
            elif n == 2:
                fruit = watermelon(v, a)
                app.fruits.append(fruit)
            fruit.x = random.randint(x-50, x)
            x += 100
    # increases the t variable for each fruit on screen
    for fruit in app.fruits:
        fruit.t += 1
        # finds the x and y variables for each fruit
        fruit.x += fruit.findX()
        fruit.y = app.height - fruit.findY()
        # if fruit is not split and falls off screen, decrease lives
        # if split, fruits follow falling motion
        if (fruit.x > app.width or fruit.y > app.height) and not fruit.split:
            app.fruits.remove(fruit)
            app.lives -= 1
            if app.lives <= 0:
                app.gameOver = True
        if fruit.split:
            fruit.y_after += 10

def redrawAll(app, canvas):
    # canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image1))
    # app.drawCamera(canvas)
    # screen for game over
    if app.gameOver:
        canvas.create_rectangle(0,0, app.width, app.height, fill="pink")
        canvas.create_text(app.width//2, app.height//2, text = "GAME OVER. PRESS R TO RESET")
        return
    # draws the fruits with respect to whether or not they've been split
    for fruit in app.fruits:
        r = fruit.r
        c = fruit.color
        if fruit.split:
            canvas.create_oval(fruit.x_after - r, fruit.y_after - r, fruit.x_after + r, fruit.y_after + r, fill=c)
        else:
            canvas.create_oval(fruit.x - r, fruit.y - r, fruit.x + r, fruit.y + r, fill = c)
    # creates mouse interaction
    if app.x != None and app.y != None:
        canvas.create_oval(app.x - app.r, app.y - app.r, app.x + app.r, app.y + app.r, fill = "purple")
    # prints the amount of lives on screen
    canvas.create_text(app.width//2, 20, text = f"THIS MANY LIVES LEFT: {app.lives}")

runApp(width =1000, height = 670)