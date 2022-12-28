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
        for id in range(len(game.Game.OccupationMap[int(self.x)][int(self.y)])):
            ent = game.Game.OccupationMap[int(self.x)][int(self.y)][id]
            if ent == self:
                del game.Game.OccupationMap[int(self.x)][int(self.y)][id]
                break

        self.x = x
        self.y = y

        game.Game.OccupationMap[int(self.x)][int(self.y)].append( self )

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
        self.eyeHeight = 4
        self.Height = 1
    def setDirection(self, dir):
        if dir > 3:
            self.direction = 0
        else:
            self.direction = dir

        self.texture = self.textures[ self.direction ]

    def setTexturePull(self, texts):
        self.textures = texts

    def doTrace(self, x, y):
        if x > game.Game.mapSize or y > game.Game.mapSize or x < 0 or y <= 0:
            out = {}
            out["HitPos"] = (0,0,0)
            out["TravelDist"] = 0
            out["TileHeight"] = 0
            out["Hit"] = True

            return out
        trg_z = game.Game.HeightMap[x][y] + self.eyeHeight
        z = game.Game.HeightMap[int(self.x)][int(self.y)]  + self.eyeHeight

        rel_x = (x - self.x)
        rel_y = (y - self.y)
        rel_z = (trg_z - z)

        init_dist = math.sqrt(rel_x ** 2 + rel_y ** 2 + rel_z ** 2)
        dist = math.sqrt(rel_x ** 2 + rel_y ** 2 + rel_z ** 2)

        rel_x = rel_x / dist
        rel_y = rel_y / dist
        rel_z = rel_z / dist

        dist_step = math.sqrt(rel_x ** 2 + rel_y ** 2 + rel_z ** 2)
        cur_y = self.y
        cur_x = self.x
        cur_z = z
        while dist > 0:

            cur_x += rel_x
            cur_y += rel_y
            cur_z += rel_z
            if cur_x > game.Game.mapSize or cur_y > game.Game.mapSize or cur_x < 0 or cur_y <= 0: break
            if cur_z <= game.Game.HeightMap[int(cur_x)][int(cur_y)]:
                #Generate out table
                out = {}
                out[ "HitPos" ] = ( cur_x, cur_y, cur_z )
                out[ "TravelDist" ] = init_dist - dist
                out[ "TileHeight" ] = game.Game.HeightMap[int(cur_x)][int(cur_y)]
                out[ "Hit" ] = True
                return out
            else:
                for ent in game.Game.OccupationMap[int(cur_x)][int(cur_y)] :
                    if ent != self and cur_z <= game.Game.HeightMap[int(cur_x)][int(cur_y)] + ent.Height:
                        out = {}
                        out["HitPos"] = (cur_x, cur_y, cur_z)
                        out["TravelDist"] = init_dist - dist
                        out["Hit"] = True
                        out["Entity"] = ent
                        return out


            dist = max( 0, dist - dist_step )

        # Generate out table
        out = {}
        out["HitPos"] = (cur_x, cur_y, cur_z)
        out["TravelDist"] = init_dist
        out["Hit"] = False

        return out




    def tick(self):
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

        TraceCheck = self.doTrace( x, y )

        print( TraceCheck )
        if not TraceCheck["Hit"]:
            self.setPos(self.x + rel_x, self.y + rel_y)



    def getYaw(self):
        return math.acos( self.velx/self.vely )


