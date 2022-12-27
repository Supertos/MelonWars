
import numpy as np
import pygame as pg
from entity import *
"""---------------------------------------------------------------------
    Perlin class
    ---------
    This class contains perlin noise functionality
---------------------------------------------------------------------"""
class Perlin:
    @staticmethod
    def interpolate( a, b, lerp ):
        return int( a + (b - a) * lerp )

    @staticmethod
    def sosi_hui_gvido( lst, x, y, lst_size ):
        if lst_size<= x: return 0
        if lst_size <= y: return 0
        return lst[x][y]

    @staticmethod
    def generate2D( size, frequency, amplitude, seed ):
        rng = np.random.default_rng( seed )
        randoms = rng.random( (int(size / frequency), int(size / frequency)) )

        out = [ [ None for _ in range(size) ] for _ in range(size) ]
        # Do random nodes to interpolate between
        for x in range( 0, size, frequency ):
            for y in range( 0, size, frequency ):
                out[x][y] = int( randoms[int(x/frequency)][int(y/frequency)]*amplitude )
        # Interpolate between them
        for x in range( size ):
            for y in range( size ):
                if out[x][y] is None: # Not a node

                    closest_x = int( x // frequency * frequency )
                    closest_y = int( y // frequency * frequency )

                    x1 = out[closest_x][closest_y] if closest_x < size and closest_y < size else 0
                    x2 = out[closest_x + frequency][
                        closest_y] if closest_x + frequency < size and closest_y < size else 0
                    x3 = out[closest_x][
                        closest_y + frequency] if closest_x < size and closest_y + frequency < size else 0
                    x4 = out[closest_x + frequency][
                        closest_y + frequency] if closest_x + frequency < size and closest_y + frequency < size else 0

                    lerp = ((x - closest_x) / frequency)
                    lerped12 = x1 + lerp * (x2 - x1)
                    lerped34 = x3 + lerp * (x4 - x3)

                    out[x][y] = int( lerped12 + ((y - closest_y) / frequency) * (lerped34 - lerped12) )
        return out

    @staticmethod
    def addLists(a,b, max_val):
        out = []
        for x in range(len(a)):
            out.append([])
            for y in range(len(a)):
                out[x].append( min(max_val,a[x][y] + b[x][y]) )
        return out


"""---------------------------------------------------------------------
    Game class
    ---------
    This class contains all game-related functionality
---------------------------------------------------------------------"""
class Game:

    seed = 0
    HeightMap = []
    mapSize = 1024
    ents = []
    cursor_x = 0
    cursor_y = 0
    game_started = False
    def __init__(self):
        pass

    @staticmethod
    def setMapSeed( seed ):
        Game.seed = seed

    @staticmethod
    def gameTick():
        for ent in Game.ents:
            ent.tick()

    @staticmethod
    def setMapCursorPos(x, y):
        Game.cursor_y = y
        Game.cursor_x = x

    @staticmethod
    def getCursorPos(x, y):
        return Game.cursor_y, Game.cursor_x

    @staticmethod
    def generateMap():
        Game.mapSize = 256
        print("Generating map!")
        OctaveA = Perlin.generate2D(Game.mapSize, 64, 200, Game.seed )
        print("Octave 128/128 generated!")
        OctaveB = Perlin.generate2D(Game.mapSize, 32, 100, Game.seed )
        print("Octave 64/64 generated!")
        OctaveC = Perlin.generate2D(Game.mapSize, 16, 50, Game.seed )
        print("Octave 32/16 generated!")
        OctaveD = Perlin.generate2D(Game.mapSize, 8, 25, Game.seed )
        print("Octave 16/4 generated!")

        Game.HeightMap = Perlin.addLists(OctaveA, Perlin.addLists(OctaveB, Perlin.addLists(OctaveC, OctaveD, 255), 255), 255)

        Ent = UnitBase()
        Ent.setTexturePull([
            pg.image.load("materials/melon_soldier.png"),
            pg.image.load("materials/melon_soldier_up.png"),
            pg.image.load("materials/melon_soldier_down.png"),
            pg.image.load("materials/melon_soldier_right.png")
        ])
        Ent.setPos(24, 24)
        #Ent.setVel(0.01, 0)
        print("Saving height map!")

        Game.game_started = True



def Entity( id ):
    return Game.ents[ id ]