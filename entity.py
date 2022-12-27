import math
import controls
import game
import pygame as pg

"""---------------------------------------------------------------------
    BaseEntity class
    ---------
    This class contains all base entity functionality
---------------------------------------------------------------------"""
class BaseEntity:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velx = 0
        self.vely = 0
        game.Game.ents.append( self )
        self.id = len(game.Game.ents)-1

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def setVel(self, x, y):
        self.velx = x
        self.vely = y

    def setTexture(self, tex):
        self.texture = pg.image.load( tex )

    def tick(self):
        cur_x = int( self.x )
        cur_y = int( self.y )

        next_x = 0
        next_y = 0
        if self.velx != 0:
            next_x = int( cur_x + self.velx/abs(self.velx) )
        if self.vely != 0:
            next_y = int( cur_y + self.vely/abs(self.vely) )

        cur_z = game.Game.HeightMap[cur_x][cur_y]
        next_z = game.Game.HeightMap[next_x][next_y]

        difficulty = next_z-cur_z

        if difficulty <= 0:
            difficulty = 1
        elif difficulty > 5:
            difficulty = 9999999999
        elif difficulty > 0:
            difficulty = 1 + difficulty/2.5
        self.setPos( self.x + self.velx/difficulty, self.y+self.vely/difficulty)

"""---------------------------------------------------------------------
    UnitBase class
    ---------
    This class handles unit operation
---------------------------------------------------------------------"""
class UnitBase(BaseEntity):
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.textures = []
        self.texture = None

    def setDirection(self, dir):
        if dir > 3:
            self.direction = 0
        else:
            self.direction = dir

        self.texture = self.textures[ self.direction ]

    def setTexturePull(self, texts):
        self.textures = texts
    def tick(self):
        #super().tick()
        self.setDirection( self.direction + 1 )
        x, y = controls.getPointedCell()

        rel_x = (x - self.x)
        rel_y = (y - self.y)

        sum = math.sqrt(rel_x**2+rel_y**2)
        rel_x = rel_x/sum
        rel_y = rel_y/sum

        if rel_x <= 0 and abs(rel_y) < 0.75: self.setDirection( 0 )
        if rel_x >= 0 and abs(rel_y) < 0.75: self.setDirection( 3 )


        if rel_x <= 0 and rel_y <= -0.75: self.setDirection( 1 )
        if rel_x >= 0 and rel_y >= 0.75: self.setDirection( 2 )

        rel_x *= 0.05
        rel_y *= 0.05
        self.setVel( rel_x, rel_y )

        self.setPos( self.x + rel_x, self.y+rel_y)
    def getYaw(self):
        return math.acos( self.velx/self.vely )


