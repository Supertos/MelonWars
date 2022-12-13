import pygame as pg

WINDOW = None
MAP = None
class Render:

    Window = None
    @staticmethod
    def makeWindow():
        global WINDOW
        WINDOW = pg.display.set_mode( (1024, 768) )
        Render.Window = WINDOW


    @staticmethod
    def drawHeightMap(map):
        global WINDOW
        global MAP

        height_map = pg.surface.Surface( (map.Size,map.Size) )
        parr = pg.PixelArray(height_map)
        for x in range( map.Size ):
            for y in range( map.Size ):
                #print( (int(250*map.Height[x][y]/256),int(223*map.Height[x][y]/256),int(173*map.Height[x][y]/256)) )
                col = (map.Height[x][y],map.Height[x][y], map.Height[x][y])
                parr[x,y] = col #(int(250*map.Height[x][y]/256),int(223*map.Height[x][y]/256),int(173*map.Height[x][y]/256))
        parr.close()
        WINDOW.blit( height_map, (0,0) )
        pg.display.flip()