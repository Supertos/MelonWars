
import Map
import Render

Render.Render.makeWindow()
MapToDraw = Map.Map( 512, 1532 )
Render.Render.drawHeightMap(MapToDraw)

print( "Map generated!" )

while True:
    pass
    #Render.Render.Window.flip()