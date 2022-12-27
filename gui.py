import pygame as pg

import controls
from Render import Render
from game import Game

global Display
Display = None
def InitializeDisplay():
    global Display
    Display = pg.display.set_mode((1024, 768), pg.SCALED)

def GetDisplay():
    global Display
    return Display




InitializeDisplay()
"""---------------------------------------------------------------------
    GuiBase
    ---------
    Base class for all GUIs
---------------------------------------------------------------------"""
class GUIBase:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.image = None
        self.focused = False
        self.hovered = False
        self.pressed = False
        self.scene = None
        self.focus_click = False    # Will game be focused on that GUI element on click? (If False there will be no focus at all)
        self.hoverable = False # Do we want to take in account if player hovers this? (Useful for images or window frames that should not be functional by itself)
    def setPos(self, x, y):
        self.x = x
        self.y = y

    def tick(self): pass
    def setX(self, x): self.x = x
    def setY(self, y): self.y = y

    def setSize(self, w, h):
        if w == self.width and h == self.height: return
        self.width = w
        self.height = h
        self.image = pg.transform.scale( self.image, (w,h))

    def setWidth(self, w):
        if w == self.width: return
        self.width = w
        self.image = pg.transform.scale(self.image, (w, self.height))

    def setHeight(self, h ):
        if h == self.height: return
        self.height = h
        self.image = pg.transform.scale( self.image, (self.width, h))

    def loadImage(self, path):
        temp_img = pg.image.load(path)
        self.image = pg.surface.Surface(temp_img.get_size(), flags=pg.SRCALPHA)
        self.image.blit( temp_img, (0,0))
        self.width, self.height = temp_img.get_size()

    def setImage(self, temp_img):
        self.image = pg.surface.Surface( temp_img.get_size(), flags=pg.SRCALPHA )
        self.image.blit( temp_img, (0,0))
        self.width, self.height = temp_img.get_size()

    def render(self, display):
        display.blit(self.image, (self.x, self.y))
    def on_delete(self):
        if self.focused:
            self.scene.GUI_ElementFocus = -1
    def on_press(self): pass
    def on_depress(self): pass
    def on_focus(self): pass
    def on_defocus(self): pass
    def on_key(self, key, mod, char, scancode): pass

"""---------------------------------------------------------------------
    Button
    ---------
    Pressable button
---------------------------------------------------------------------"""
class Button(GUIBase):
    def __init__(self):
        super().__init__()
        self.pressed_image = None
        self.depressed_image = None
        self.NextScene = None
        self.hoverable = True

    def setSize(self, w, h):
        if w == self.width and h == self.height: return
        self.width = w
        self.height = h
        self.pressed_image = pg.transform.scale( self.pressed_image, (w,h))
        self.depressed_image = pg.transform.scale( self.depressed_image, (w,h))

    def setWidth(self, w):
        if w == self.width: return
        self.width = w
        self.pressed_image = pg.transform.scale( self.pressed_image, (w,self.height))
        self.depressed_image = pg.transform.scale( self.depressed_image, (w, self.height))

    def setHeight(self, h ):
        if h == self.height: return
        self.height = h

        self.pressed_image = pg.transform.scale( self.pressed_image, (self.width,h))
        self.depressed_image = pg.transform.scale( self.depressed_image, (self.width,h))

    def loadImage(self, pressed, depressed):
        temp_img = pg.image.load(pressed)
        self.pressed_image = pg.surface.Surface(temp_img.get_size(), flags=pg.SRCALPHA)
        self.pressed_image.blit( temp_img, (0,0))

        temp_img = pg.image.load(depressed)
        self.depressed_image = pg.surface.Surface(temp_img.get_size(), flags=pg.SRCALPHA)
        self.depressed_image.blit( temp_img, (0,0))

        self.width, self.height = temp_img.get_size()
    def setNextScene(self, Scene):
        self.NextScene = Scene
    def setImage(self, pressed, depressed):
        self.pressed_image = pg.surface.Surface( pressed.get_size(), flags=pg.SRCALPHA )
        self.pressed_image.blit( pressed, (0,0))
        self.depressed_image = pg.surface.Surface( depressed.get_size(), flags=pg.SRCALPHA )
        self.depressed_image.blit( depressed, (0,0))

        self.width, self.height = pressed.get_size()

    def render(self, display):
        if self.pressed:
            display.blit(self.pressed_image, (self.x, self.y))
        else:
            display.blit(self.depressed_image, (self.x, self.y))
    def on_press(self):
        self.scene.RequireUpdate = True
    def on_depress(self):
        self.scene.RequireUpdate = True
        self.action()
        if self.NextScene is not None:
            SetCurrentScene( self.NextScene )
    def setAction(self, action):
        funcType = type(self.action)
        self.action = funcType(action, self)

    def action(self):
        pass

"""---------------------------------------------------------------------
    QuitButton
    ---------
    Button that quits
---------------------------------------------------------------------"""
class QuitButton(Button):
    def action(self):
        quit()
"""---------------------------------------------------------------------
    Text
    ---------
    Simple text
---------------------------------------------------------------------"""
class Text(GUIBase):

    def __init__(self):
        super().__init__()
        pg.font.init()
        self.Text = ""
        self.Font = pg.font.Font('materials/text_main.ttf', 16)
    def setText(self, text):
        self.Text = text
        self.surf = self.Font.render(text, False, (0, 0, 0))
    def render(self, display):
        display.blit(self.surf, (self.x, self.y))


"""---------------------------------------------------------------------
    TextButton
    ---------
    Pressable button with text on it
---------------------------------------------------------------------"""
class TextButton(Button):
    def __init__(self):
        super().__init__()
        pg.font.init()
        self.Text = ""
        self.TextSurf = None
        self.TextSurfB = None
        self.FontPressed = pg.font.Font('materials/text_main_b.ttf', 16)
        self.FontDepressed = pg.font.Font('materials/text_main.ttf', 16)
    def setText(self, text):
        self.Text = text
        self.TextSurfB = self.FontPressed.render(text, False, (0, 0, 0))
        self.TextSurf = self.FontDepressed.render(text, False, (0, 0, 0))
    def render(self, display):
        w, h = self.TextSurf.get_size()

        x = self.x + self.width/2 - w/2
        y = self.y + self.height/2 - h/2


        if self.pressed:
            display.blit(self.pressed_image, (self.x, self.y))
            display.blit(self.TextSurfB, (x, y))
        else:
            display.blit(self.depressed_image, (self.x, self.y))
            display.blit(self.TextSurf, (x, y))

"""---------------------------------------------------------------------
    TextInput
    ---------
    Provides text input/output
---------------------------------------------------------------------"""
class TextInput(GUIBase):
    def __init__(self):
        super().__init__()
        pg.font.init()
        self.Text = ""
        self.DefaultText = ""
        self.TextSurf = None
        self.Font = pg.font.Font('materials/text_main_b.ttf', 12)
        self.focus_click = True
        self.hoverable = True

    def on_defocus(self):
        pass

    def on_focus(self):
        pass

    def setText(self, text):
        self.Text = text
        self.TextSurf = self.Font.render(text, False, (0, 0, 0))

    def render(self, display):
        w, h = self.TextSurf.get_size()

        x = self.x + 32
        y = self.y + self.height/2 - h/2

        display.blit(self.image, (self.x, self.y))

        display.blit(self.TextSurf, (x, y))

    def on_key(self, key, mod, char, scancode):
        if key == 8: # Backspace
            self.Text = self.Text[:-1]
        else:
            self.Text = self.Text + char
        self.TextSurf = self.Font.render(self.Text, False, (0, 0, 0))

        self.scene.RequireUpdate = True


"""---------------------------------------------------------------------
    MapCam
    ---------
    This special GUI object renders map to the screen
---------------------------------------------------------------------"""
class MapCam(GUIBase):
    def __init__(self):
        super().__init__()
        self.CamX = 0
        self.CamY = 0
        self.CellSize = 2 #How much of a screen space occupies every cell
        self.focus_click = True
        self.hoverable = True

        self.Heights = [ None for i in range(256) ]
        self.updateTileMap()
        self.Chunks = {}

    def updateTileMap(self):
        for i in range(256):
            surf = pg.surface.Surface( (self.CellSize, self.CellSize) )
            surf.fill( self.calculateColor(i) )
            self.Heights[ i ] = surf


    def calculateColor(self, height):
        if height > 128:
            return (int(250 * height / 256), int(223 * height / 256), int(173 * height / 256))
        else:
            mod = max(0.5, int(height / 64))
            return (25 * mod, 50 * mod, 127 * mod)

    def setSize(self, w, h):
        if w == self.width and h == self.height: return
        self.width = w
        self.height = h

    def tick(self):
        if controls.isKeyPressed( 1073741906 ) :
            self.CamY = max( 0, min( Game.mapSize-self.height//self.CellSize, self.CamY - 2/self.CellSize ) )
        if controls.isKeyPressed( 1073741904 ) :
            self.CamX = max( 0, min( Game.mapSize-self.width//self.CellSize, self.CamX - 2/self.CellSize ) )
        if controls.isKeyPressed( 1073741905 ) :
            self.CamY = max( 0, min( Game.mapSize-self.height//self.CellSize, self.CamY + 2/self.CellSize ) )
        if controls.isKeyPressed( 1073741903 ):
            self.CamX = max( 0, min( Game.mapSize-self.width//self.CellSize, self.CamX + 2/self.CellSize ) )

    def on_focus(self):
        pass

    def chunkLoad(self, x, y):
        return Render.renderChunk( (x,y), self.CellSize )

    def render(self, display):

        #Render height map first
        surf = pg.surface.Surface((self.width, self.height), flags=pg.SRCALPHA)

        startChunk = (self.CamX/32, self.CamY/32)
        endChunk = (self.CamX//32 + int( (self.width/self.CellSize)//32+1 ), self.CamY//32 + int((self.height/self.CellSize)//32+1)  )


        s_x, s_y = startChunk
        e_x, e_y = endChunk

        chunk_float_x = int( s_x%1*self.CellSize )
        chunk_float_y = int( s_y%1*self.CellSize )

        float_x = int( self.CamX%1*self.CellSize )
        float_y = int( self.CamY%1*self.CellSize )

        for x in range( int(s_x), int(e_x)+1 ):
            for y in range( int(s_y), int(e_y)+1 ):
                chunk = ( x, y )
                if chunk not in self.Chunks:
                    self.Chunks[chunk] = self.chunkLoad( x, y )
                chunk_surf = self.Chunks[ chunk ]

                real_x = (x*32-self.CamX)*self.CellSize
                real_y = (y*32-self.CamY)*self.CellSize
                surf.blit( chunk_surf, ( chunk_float_x + real_x, chunk_float_y + real_y))

        #Render selection rectangle
        sel_surf = pg.surface.Surface((self.CellSize, self.CellSize), flags=pg.SRCALPHA)
        sel_surf.fill( (0,0,0,100) )

        #Compute cell we pointed at:
        x, y = controls.getMousePos()

        world_x = int(self.CamX) + ( x + float_x ) // self.CellSize
        world_y = int(self.CamY) + ( y + float_y ) // self.CellSize

        #Compute that's cell screen position
        scr_x = ( world_x - int( self.CamX ) ) * self.CellSize - float_x
        scr_y = ( world_y - int( self.CamY ) ) * self.CellSize - float_y



        controls.selectCell( world_x, world_y )

        #surf.blit( sel_surf, (scr_x,scr_y))


        #Render entities
        toDraw = Game.ents#self.cullEnts()

        for ent in toDraw:
            w, h = ent.texture.get_size()

            real_w = w*self.CellSize/64
            real_h = h*self.CellSize/64
            surf_to_blit = pg.transform.scale(ent.texture, (real_w, real_h))


            real_x = ( ent.x - self.CamX )*self.CellSize + int(real_w/2)
            real_y = ( ent.y - self.CamY )*self.CellSize - int(real_h/2)
            surf.blit( surf_to_blit, (real_x, real_y) )

        display.blit(surf, (self.x, self.y))

    def cullEnts( self ):
        out = []
        CullSizeX = self.CamX + int(self.width/self.CellSize)
        CullSizeY = self.CamY + int(self.height/self.CellSize)
        for ent in Game.ents:
            if self.CamX < ent.x < CullSizeX and self.CamY < ent.y < CullSizeY:
                out.append( ent )

        return out

    def on_key(self, key, mod, char, scancode):

        if key == 1073741911:
            self.CellSize *= 2
            self.Chunks = {}
        elif key == 1073741910:
            self.CellSize = int( max(1, self.CellSize * 0.5))
            self.Chunks = {}
        self.updateTileMap()




from scene import *