from gui import *

from scene import *
import pygame as pg


#pg.display.toggle_fullscreen()

TICK = 0
Display = GetDisplay()
while True:
    TICK += 1
    Cur_Scene = GetCurrentScene()
    # Process interrupts
    while pg.event.peek:
        event = pg.event.poll()
        if event.type == pg.NOEVENT: break
        if event.type == pg.QUIT:
            quit(0)
        elif event.type == pg.MOUSEMOTION:
            if Cur_Scene.LastGUIElementID > -1:
                mouse_x, mouse_y = event.pos

                old_id = Cur_Scene.GUI_ElementHover
                Cur_Scene.GUI_ElementHover = -1

                for id in range(1, len(Cur_Scene.GUI_Elements)):
                    el = Cur_Scene.GUI_Elements[id]
                    if el.x < mouse_x < el.x + el.width and el.y < mouse_y < el.y + el.height and el.hoverable:
                        el.hovered = True
                        Cur_Scene.GUI_ElementHover = id
                        break

                if old_id != Cur_Scene.GUI_ElementHover:
                    if Cur_Scene.GUI_Elements[old_id].pressed:
                        Cur_Scene.GUI_Elements[old_id].pressed = False
                        Cur_Scene.GUI_Elements[Cur_Scene.GUI_ElementHover].on_depress()
                    Cur_Scene.GUI_Elements[old_id].hovered = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if Cur_Scene.GUI_ElementHover > -1:
                Cur_Scene.GUI_Elements[Cur_Scene.GUI_ElementHover].pressed = True
                Cur_Scene.GUI_Elements[Cur_Scene.GUI_ElementHover].on_press()
        elif event.type == pg.MOUSEBUTTONUP:
            if Cur_Scene.GUI_ElementHover != Cur_Scene.GUI_ElementFocus and Cur_Scene.GUI_ElementFocus > -1:
                Cur_Scene.GUI_ElementFocus = Cur_Scene.GUI_ElementHover
                Cur_Scene.GUI_Elements[Cur_Scene.GUI_ElementFocus].focused = False
                Cur_Scene.GUI_Elements[Cur_Scene.GUI_ElementFocus].on_defocus()

            if Cur_Scene.GUI_ElementHover > -1:
                el = Cur_Scene.GUI_Elements[Cur_Scene.GUI_ElementHover]
                el.pressed = False
                el.on_depress()
                if el.focus_click:
                    Cur_Scene.GUI_ElementFocus = Cur_Scene.GUI_ElementHover
                    el.focused = True
                    el.on_focus()
        elif event.type == pg.KEYUP:
            if Cur_Scene.GUI_ElementFocus > -1:
                Cur_Scene.GUI_Elements[Cur_Scene.GUI_ElementFocus].on_key( event.key, event.mod, event.unicode, event.scancode )

    # Render all stuff
    if Cur_Scene.RequireUpdate:
        Cur_Scene.render()
        Cur_Scene.RequireUpdate = False
        for el in Cur_Scene.GUI_Elements:
            el.render(Display)
        pg.display.flip()
    # Do scene tick
    Cur_Scene.tick(TICK)
