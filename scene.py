import math
from gui import *
import pygame as pg

from gui import GetDisplay


def GetCurrentScene():
    global Cur_Scene
    return Cur_Scene

def SetCurrentScene(scene):
    global Cur_Scene
    Cur_Scene = scene
    Cur_Scene.display = GetDisplay()
    scene.init()



"""---------------------------------------------------------------------
    SceneBase
    ---------
    Base class for all scenes
---------------------------------------------------------------------"""
class SceneBase:
    def __init__(self):
        self.GUI_Elements = []
        self.GUI_ElementFocus = -1
        self.GUI_ElementHover = -1
        self.LastGUIElementID = -1
        self.RequireUpdate = True
        self.display = None
    def init(self): pass
    def render(self): pass
    def tick(self, tick): pass
    def quit(self): pass
    def addRenderElement(self, element):
        self.GUI_Elements.append( element )
        element.scene = self
        self.LastGUIElementID += 1
        self.RequireUpdate = True
        return self.LastGUIElementID
    def killRenderElement(self, el_id):
        self.GUI_Elements[ el_id ].on_delete()
        del self.GUI_Elements[ el_id ]
        self.RequireUpdate = True


"""---------------------------------------------------------------------
    SceneStart
    ---------
    Base class for all scenes
---------------------------------------------------------------------"""
class SceneStart(SceneBase):
    def init(self):
        self.logoY = 64

        self.logo = GUIBase()
        self.logo.setPos(256, self.logoY)
        self.logo.loadImage("materials/logo_512x256px.png")
        self.addRenderElement(self.logo)

        self.startgame = TextButton()
        self.startgame.setPos(512-128, 256)
        self.startgame.loadImage("materials/button256px_pressed.png", "materials/button256px.png")
        self.startgame.setText("New Game")
        self.startgame.setNextScene(SceneMapSetup())
        self.addRenderElement(self.startgame)

        self.quit = QuitButton()
        self.quit.setPos(1024 - 32, 0)
        self.quit.loadImage("materials/exit_button_pressed.png", "materials/exit_button_unpressed.png")
        self.addRenderElement(self.quit)

    def tick(self, tick):
        self.display.fill( (250, 223, 173) )
        self.logoY = 64+math.sin(tick/1000)*32
        self.logo.setY( self.logoY )
        self.RequireUpdate = True


"""---------------------------------------------------------------------
    SceneMapSetup
    ---------
    Scene for map creation
---------------------------------------------------------------------"""
class SceneMapSetup(SceneBase):
    def init(self):
        self.display.fill( (250, 223, 173) )

        self.seedtext = Text()
        self.seedtext.setPos(32, 64)
        self.seedtext.setText("Seed")
        self.addRenderElement(self.seedtext)

        self.seed = TextInput()
        self.seed.setPos(32, 96)
        self.seed.setText("")
        self.addRenderElement(self.seed)
        self.seed.loadImage("materials/input512px.png")
    #def tick(self, tick):



SetCurrentScene(SceneStart())