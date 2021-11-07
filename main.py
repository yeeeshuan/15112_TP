from cmu_112_graphics import *
import random
import math

class fruit(object):
    def __init__(self, v, a):
        self.v = v
        self.t = 0
        self.a = a
        self.split = False
        self.xl = None
        self.yl = None
        self.xr = None
        self.yr = None
        self.x = random.randint(100, 300)

    def findX(self):
        return (self.v * math.cos(self.a) * self.t)

    def findY(self):
        return (self.v * math.sin(self.a) * self.t - 10 * self.t ** 2)

    def setSplit(self):
        xl = self.x
        yl = self.y
        ylr = self.x

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

def appStarted(app):
    app.image1 = app.loadImage('background.jpg')
    app.image2 = app.scaleImage(app.image1, 2/3)
    app.fruits = []
    app.timerDelay = 100
    app.x = None
    app.y = None
    app.r = 10
    app.time = 1

#mousepressed
def mouseMoved(app, event):
    app.x = event.x
    app.y = event.y
    for fruit in app.fruits:
        if sliced(fruit.x, fruit.y, app.x, app.y, fruit.r):
            #fruit.split = True
            app.fruits.remove(fruit)

def sliced(x1, y1, x2, y2, r):
    return distance(x1,y1,x2,y2) <= r

def distance(x1,y1,x2,y2):
    return ((x2-x1) ** 2 + (y2- y1) ** 2) ** (1/2)

#timer fired
def timerFired(app):
    app.time += 1
    if app.time % 20 == 0:
        n = random.randint(0,2)
        v = random.randint(80,100)
        a = random.randint(75,85)
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
    for fruit in app.fruits:
        fruit.t += 1

def redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image1))
    for fruit in  app.fruits:
        r = fruit.r
        c = fruit.color
        if fruit.split == True:
            fruit.setSplit()
            fruit.xl -= 1
            fruit.xr -= 1
            fruit.ylr += 1
            canvas.create_oval(fruit.xl - r, fruit.ylr - r, fruit.xl + r, fruit.ylr + r, fill=c)
            canvas.create_oval(fruit.xr - r, fruit.ylr - r, fruit.xr + r, fruit.ylr + r, fill=c)

        fruit.x += fruit.findX()
        fruit.y =  app.height - fruit.findY()

        canvas.create_oval(fruit.x - r, fruit.y - r, fruit.x + r, fruit.y + r, fill = c)
        if app.x != None and app.y != None:
            canvas.create_oval(app.x - app.r, app.y - app.r, app.x + app.r, app.y + app.r, fill = "purple")

runApp(width = 1000, height = 1000)