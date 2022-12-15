import pygame as pg


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
        self.hoverable = True # Do we want to take in account if player hovers this? (Useful for images or window frames that should not be functional by itself)
    def setPos(self, x, y):
        self.x = x
        self.y = y

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
        if self.NextScene is None:
            self.action()
        else:
            SetCurrentScene( self.NextScene )

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

    def on_defocus(self):
        print("Defocused!")

    def on_focus(self):
        print("Focused!")

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


from scene import *