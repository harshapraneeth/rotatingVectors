import math
import pygame as pg
import random
import time

size = 800  #window size
nvectors = 10 #number of vectors
lrange = 150 #max vector length
time_loss = 0.025 #decrease it or set it to zero if the program lags, or increase it if the program is too fast


hsize = size//2

def ma(p): return (p[0]+hsize, hsize-p[1])

def dist(p1,p2): return int(math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))

class Vector:
    def __init__(self, length, slope, speed, axis, origin):
        self.length, self.slope, self.speed = length, slope, speed
        self.pos, self.axis, self.origin = (0, 0), axis, origin
    def determinePosition(self):
        self.pos = (math.cos(self.slope)*self.length + self.origin[0], math.sin(self.slope)*self.length + self.origin[1])
    def draw(self):
        pg.draw.line(screen, (255,255,255), ma(self.origin), ma(self.pos), 2)
        p1 = (math.cos(self.slope-5*math.pi/6)*10 + self.pos[0], math.sin(self.slope-5*math.pi/6)*10 + self.pos[1])
        p2 = (math.cos(self.slope+5*math.pi/6)*10 + self.pos[0], math.sin(self.slope+5*math.pi/6)*10 + self.pos[1])
        pg.draw.line(screen, (255,255,255), ma(self.pos),ma(p1), 2)
        pg.draw.line(screen, (255,255,255), ma(self.pos),ma(p2), 2)
        if not self.axis:
            pg.draw.circle(screen, (255,0,0), ma((int((self.pos[0]+self.origin[0])//2),int((self.pos[1]+self.origin[1])//2))), dist(self.origin,self.pos)//2+1, 1)
    def rotate(self):
        self.slope += self.speed
        self.determinePosition()

xaxis = Vector(hsize, 0, 0, True, (0,0))
xaxis.determinePosition()
yaxis = Vector(hsize, math.pi/2, 0, True, (0,0))
yaxis.determinePosition()
nxaxis = Vector(hsize, math.pi, 0, True, (0,0))
nxaxis.determinePosition()
nyaxis = Vector(hsize, -math.pi/2, 0, True, (0,0))
nyaxis.determinePosition()

vecs = [Vector(random.randint(0,lrange), math.pi*random.uniform(-2,2), math.pi*random.uniform(-0.025,0.025),False, (0,0)) for i in range(nvectors)]
pps = []

def joinVectors():
    o = (0,0)
    for i in range(len(vecs)):
        vecs[i].origin = o
        vecs[i].determinePosition()
        o = vecs[i].pos

def trace(v):
    p = ma(v.pos)
    pps.append((int(p[0]), int(p[1])))
    n = len(pps)
    if n>1:
        for i in range(n-1):
            pg.draw.line(screen,(0,255,0),pps[i],pps[i+1],1)

pg.init()
screen = pg.display.set_mode((size,size))
pg.display.set_caption('Fourier Draws')

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit()
    screen.fill((0, 0, 0))
    xaxis.draw()
    nxaxis.draw()
    yaxis.draw()
    nyaxis.draw()
    joinVectors()
    for i in vecs:
        i.draw()
        i.rotate()
    trace(vecs[-1])
    pg.display.update()
    time.sleep(time_loss)
