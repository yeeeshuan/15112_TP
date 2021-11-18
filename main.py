from cmu_112_graphics_openCV import *
import random
import math
import cv2

# fruit class
class fruit(object):
    def __init__(self, v, a):
        self.v = v
        self.t = 0
        self.a = a
        self.split = False
        self.splitPos = None
        #for after fruit is split and individual pieces
        self.x_after = None
        self.y_after = None
        self.xr_after = None
        self.yr_after = None
        self.lstart = 180
        self.rstart = 180
        self.t_after = 0

    # finds the x coordinate with respect to horizontal vectors
    def findX(self):
        return (self.v * math.cos(self.a) * self.t)

    # finds the x coordinates after split
    def findXAfter(self):
        return (10 * math.cos(330 * (math.pi/180)) * self.t_after)

    # finds the y coordinate with respect to vertical vectors
    def findY(self):
        return (self.v * math.sin(self.a) * self.t - 3 * self.t ** 2)

    # finds the y coordinates after split
    def findYAfter(self):
        return (3 * math.sin(330 * (math.pi/180)) * self.t - 0.5 * self.t ** 2)

# subclasses of different fruits
# contains radius and color attributes
#apple class
class apple(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r = 50
        self.color = "red"

#orange class
class orange(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r= 60
        self.color = "orange"

#watermelon class
class watermelon(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r = 80
        self.color = "green"

#blueberry class
class blueberry(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r = 40
        self.color = "blue"

#pineapple class
class pineapple(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r = 50
        self.color = "yellow"

#kiwi class
class kiwi(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r = 50
        self.color = "brown"

#bomb class
class bomb(fruit):
    def __init__(self,v,a):
        super().__init__(v,a)
        self.r = 50
        self.color = "black"

#splash class
class splash(object):
    def __init__(self, x, y, r, a, rad):
        self.org_X = x
        self.org_Y = y
        self.x  = x
        self.y = y
        self.r = r
        self.a = a
        self.t = 0
        self.rad = rad

    def findXAfter(self):
        return (3 * math.cos(self.a * (math.pi/180)) * self.t)

    def findYAfter(self):
        return (3 * math.sin(self.a * (math.pi/180)) * self.t - 6 * self.t ** 2)

# appstarted
def appStarted(app):
    app.image1 = app.loadImage('background.jpg')
    app.image2 = app.scaleImage(app.image1,1)
    app.fruits = []
    app.timerDelay = 100
    app.x = None
    app.y = None
    app.r = 10
    app.time = 1
    app.cameraOpen = True
    app.lives = 10
    app.gameOver = False
    app.score = 0
    app.tstart = 0
    app.combo = False
    app.critical_hit = False
    app.hitX = None
    app.hitY = None
    app.splashes = []

# mouseMoved in substitute for cameraFired
def mouseMoved(app, event):
    app.combo = False
    app.critical_hit = False
    app.x = event.x
    app.y = event.y

    #if fruit is sliced, set coordinates for falling and split to True
    for fruit in app.fruits:
        if fruit.split == False and sliced(fruit.x, fruit.y, app.x, app.y, fruit.r):
            #stores position that fruit is hit
            app.hitX = app.x
            app.hitY = app.y
            #creates splash animation
            for x in range(5):
                a = random.randint(0, 180)
                r = random.randint(5, 15)
                nsplash = splash(app.hitX, app.hitY, fruit.r, a, r)
                app.splashes.append(nsplash)
                print(len(app.splashes))
            #finds the angle of split for split animation
            angle = math.degrees(math.atan((app.hitY - fruit.y)/(app.hitX - fruit.x)))

            if app.hitX > fruit.x and app.hitY < fruit.y:
                fruit.lstart = angle
                fruit.rstart = angle

            if app.hitX < fruit.x and app.hitY < fruit.y:
                fruit.lstart = 180 - angle
                fruit.rstart = 180 - angle

            if app.hitX < fruit.x and app.hitY > fruit.y:
                fruit.lstart = 270 - angle
                fruit.rstart = 170 - angle

            if app.hitX > fruit.x and app.hitY < fruit.y:
                fruit.lstart = 360 - angle
                fruit.rstart = 360 - angle

            #if hit near middle of fruit, critical hit
            if abs(app.hitY - fruit.y) <= 10:
                app.score += 10
                app.critical_hit = True
                print("CRITICAL HIT")
            else:
                app.score += 1
            if isinstance(fruit, bomb):
                app.lives -= 1
                fruit.hit = True

            #sets coordinates and split
            fruit.x_after = app.hitX
            fruit.y_after = app.hitY
            fruit.xr_after = app.hitX
            fruit.yr_after = app.hitY
            fruit.split = True
"""
# tracks the brightest pixel on the screen as tracker
# combined tacking code from https://www.pyimagesearch.com/2014/09/29/
# in collaboration with Alina Chen (alinache) 
# finding-brightest-spot-image-using-python-opencv/ with 112 graphics
def cameraFired(app):
    app.combo = False
    app.critical_hit = False
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
            app.hitX = app.x
            app.hitY = app.y
            for x in range(5):
                a = random.randint(0, 359)
                nsplash = splash(app.hitX, app.hitY, fruit.r, a)
                app.splashes.append(nsplash)
            # finds the angle of split for split animation
            angle = math.degrees(math.atan((app.hitY - fruit.y) / (app.hitX - fruit.x)))

            if app.hitX > fruit.x and app.hitY < fruit.y:
                fruit.lstart = angle
                fruit.rstart = angle

            if app.hitX < fruit.x and app.hitY < fruit.y:
                fruit.lstart = 180 - angle
                fruit.rstart = 180 - angle

            if app.hitX < fruit.x and app.hitY > fruit.y:
                fruit.lstart = 270 - angle
                fruit.rstart = 170 - angle

            if app.hitX > fruit.x and app.hitY < fruit.y:
                fruit.lstart = 360 - angle
                fruit.rstart = 360 - angle

            if abs(app.hitY - fruit.y) <= 10:
                app.score += 10
                app.critical_hit = True
            else:
                app.score += 1

            if isinstance(fruit, bomb):
                app.lives -= 1
                fruit.hit = True
            fruit.x_after = app.hitX
            fruit.y_after = app.hitY
            fruit.xr_after = app.hitX
            fruit.yr_after = app.hitY
            fruit.split = True
"""
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
    gap = 30
    x = 200
    total = random.randint(3,5)
    # randomly generates three fruits to be thrown from bottom of screen
    if app.time % gap == 0:
        for i in range(total):
            #projectile motion variables
            n = random.randint(0,6)
            v = random.randint(70,80)
            a = random.randint(88,90)
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
            elif n == 3:
                fruit = pineapple(v, a)
                app.fruits.append(fruit)
            elif n == 4:
                fruit = blueberry(v, a)
                app.fruits.append(fruit)
            elif n == 5:
                fruit = kiwi(v, a)
                app.fruits.append(fruit)
            elif n == 6:
                fruit = bomb(v, a)
                app.fruits.append(fruit)
            fruit.x = random.randint(x-50, x)
            x += 150

    # increases the t variable for each fruit on screen
    count = 0
    for fruit in app.fruits:
        fruit.t += 1
        # finds the x and y variables for each fruit
        fruit.x += fruit.findX()
        fruit.y = app.height - fruit.findY()
        # if fruit is not split and falls off screen, decrease lives
        # if split, fruits follow falling motion
        if (fruit.x > app.width or fruit.y > app.height):
            if not fruit.split and not isinstance(fruit, bomb):
                app.lives -= 1
                if app.lives <= 0:
                    app.gameOver = True
            app.fruits.remove(fruit)

        #finds the coordinates of split fruit
        if fruit.split and not isinstance(fruit, bomb):
            count += 1
            if count == 1:
                app.t_after = app.time
            fruit.t_after += 1
            fruit.x_after -= fruit.findXAfter()
            fruit.y_after -= fruit.findYAfter()
            fruit.xr_after += fruit.findXAfter()
            fruit.yr_after -= fruit.findYAfter()
            if (fruit.x_after > app.width or fruit.xr_after > app.width
                or fruit.y_after > app.height or fruit.yr_after > app.height):
                try:
                    app.fruits.remove(fruit)
                except:
                    pass
                # if three fruits hit under .3 seconds, combo
        if count == total:
            if app.t_after - app.time <= total * 100:
                app.combo = True

    #finds the coordinates of splash bubbles
    for splash in app.splashes:
        splash.t += 1
        splash.x = splash.org_X + 10 - splash.findXAfter()
        splash.y = splash.org_Y + 10 - splash.findYAfter()
        if distance(splash.x, splash.y, splash.org_X, splash.org_Y) > splash.r + 30:
            app.splashes.remove(splash)

def redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    # app.drawCamera(canvas)
    # screen for game over
    if app.gameOver:
        canvas.create_rectangle(0,0, app.width, app.height, fill="pink")
        canvas.create_text(app.width//2, app.height//2, text = "GAME OVER. PRESS R TO RESET")
        return
    # draws the fruits with respect to whether or not they've been split
    for fruit in app.fruits:
        c = fruit.color
        r = fruit.r
        if fruit.split:
            if isinstance(fruit, bomb):
                r += 3
                fruit.r = r
                canvas.create_oval(fruit.x - r, fruit.y - r , fruit.x + r, fruit.y + r, fill= "red")
                canvas.create_oval(fruit.x - r/2, fruit.y - r/2, fruit.x + r/2, fruit.y + r/2, fill="orange")
                canvas.create_oval(fruit.x - r/4, fruit.y - r/4, fruit.x + r/4, fruit.y + r/4, fill="yellow")
            else:
                fruit.lstart += 10
                fruit.rstart -= 10
                canvas.create_arc(fruit.x_after - r/2, fruit.y_after - r/2, fruit.x_after + r/2, fruit.y_after + r/2,
                                 start = fruit.lstart, extent = 180, fill = c)
                canvas.create_arc(fruit.xr_after - r/2, fruit.yr_after - r/2, fruit.xr_after + r/2, fruit.yr_after + r/2,
                                start = fruit.rstart, extent = -180, fill = c)
        else:
            try :
                canvas.create_oval(fruit.x - r, fruit.y - r, fruit.x + r, fruit.y + r, fill = c)
                if isinstance(fruit, bomb):
                    canvas.create_line(fruit.x - r/2, fruit.y - r/2, fruit.x + r/2, fruit.y + r/2, fill="red", width = 5)
                    canvas.create_line(fruit.x - r / 2, fruit.y + r / 2, fruit.x + r / 2, fruit.y - r / 2, fill="red",
                                   width=5)
            except:
                pass

    # creates splashes if cut
    for splash in app.splashes:
        r = splash.rad
        canvas.create_oval(splash.x - r , splash.y - r, splash.x + r, splash.y + r, fill = "blue")
    # creates mouse interaction
    if app.x != None and app.y != None:
        canvas.create_oval(app.x - app.r, app.y - app.r, app.x + app.r, app.y + app.r, fill = "purple")
    # prints the amount of lives on screen
    canvas.create_text(15, 20, text = f"THIS MANY LIVES LEFT: {app.lives}")
    canvas.create_text(app.width - 50 , 20, text=f"SCORE: {app.score, len(app.fruits)}")
    # prints combos and critical hits
    if app.critical_hit:
        canvas.create_text(app.width - 50 , 40, text="CRITICAL HIT", fill="yellow", font="Helvetica 15 bold underline")
    if app.combo:
        canvas.create_text(app.width - 50, 40, text="COMBO", fill="yellow", font="Helvetica 15 bold underline")

runApp(width =1000, height = 670)