import pygame as pg
import numpy as np
from game import *
class Render:

    water_color = (194, 212, 198)
    field_color = (246, 209, 157)
    forest_color = (244, 193, 130)

    @staticmethod
    def getRandoms():
        rng = np.random.default_rng(8192)
        return rng.random( (256, 1) )
    @staticmethod
    def getTileColor(height, type):
        if type == "water":
            r,g,b = Render.water_color
            return (128+r*height/256, 128+g*height/256, 128+b*height/256)
        elif type == "field":
            r,g,b = Render.field_color
            return (int(r*(128+height)/512), int(g*(128+height)/512), int(b*(128+height)/512))
        elif type == "forest":
            r,g,b = Render.forest_color
            return (r*height/256, g*height/256, b*height/256)

    #A very expensive function
    @staticmethod
    def renderChunk( chunk_id, scale ):
        chunk = pg.surface.Surface( (scale*32,scale*32), flags=pg.SRCALPHA )
        chunk_x, chunk_y = chunk_id
        base_x = chunk_x*32
        base_y = chunk_y*32
        randoms = Render.getRandoms()
        heights = Game.HeightMap
        tile = pg.surface.Surface( (scale,scale) )
        for x in range( base_x, base_x + 32 ):
            for y in range( base_y, base_y + 32 ):
                if x > Game.mapSize-1 or y > Game.mapSize-1:
                    height = 0
                else:
                    height = heights[x][y]
                if height < 128:
                    tile.fill( Render.getTileColor(height, "water") )
                elif height >= 128 and height < 136 or height > 200 and height < 240:
                    tile.fill( Render.getTileColor(height, "field") )
                else:
                    tile.fill( Render.getTileColor(height, "forest") )

                draw_x = x % 32
                if draw_x == 32: draw_x = 0

                draw_y = y % 32
                if draw_y == 32: draw_y = 0
                chunk.blit( tile, (draw_x*scale, draw_y*scale) )
        return chunk

