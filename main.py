from cmu_112_graphics import *
import random
import math

class fruit(object):
    def __init__(self, v, a, pos):
        self.v = v
        self.t = 0
        self.a = a
        self.pos = pos

    def findX(self):
        return self.v * math.cos(self.a) * self.t

    def findY(self):
        return self.v * math.cos(self.a) * self.t + 4.9 * self.t ** 2

class apple(fruit):
    def __init__(self,v,a, pos):
        super().__init__(v,a, pos)
        self.r = 40
        self.color = "red"

class orange(fruit):
    def __init__(self,v,a, pos):
        super().__init__(v,a, pos)
        self.r= 50
        self.color = "orange"

class watermelon(fruit):
    def __init__(self,v,a, pos):
        super().__init__(v,a, pos)
        self.r = 60
        self.color = "green"

def appStarted(app):
    app.fruits = []
    app.timerDelay = 1000
    app.x = None
    app.y = None
    app.r = 10
    app.time = 1

#mousepressed
def mouseMoved(app, event):
    app.x = event.x
    app.y = event.y

#timer fired
def timerFired(app):
    app.time += 1
    if app.time % 10:
        app.timerDelay - 100
    n = random.randint(0,2)
    v = random.randint(50,100)
    a = random.randint(0,10)
    pos =  random.randint(0,1)
    if n == 0:
        fruit = apple(v,a, pos)
        app.fruits.append(fruit)
    elif n == 1:
        fruit = orange(v, a, pos)
        app.fruits.append(fruit)
    elif n == 2:
        fruit = watermelon(v, a, pos)
        app.fruits.append(fruit)
    for fruit in app.fruits:
        fruit.t += 1


def redrawAll(app, canvas):
    startY = random.randint(app.height//2, app.height)
    for fruit in  app.fruits:
        if fruit.pos == 0:
            x =  fruit.findX()
            y = fruit.findY()
        elif fruit.pos ==  1:
            x = app.width - fruit.findX()
            y = fruit.findY()
        r = fruit.r
        c = fruit.color
        canvas.create_oval(x - r, y - r, x + r, y + r, fill = c)
        if app.x != None and app.y != None:
            canvas.create_oval(app.x - app.r, app.y - app.r, app.x + app.r, app.y + app.r, fill = "purple")

runApp(width = 800, height = 800)
