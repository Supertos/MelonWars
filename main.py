
import Map
import Render
import cProfile
#Render.Render.makeWindow()
#MapToDraw = Map.Map( 1024, 567586585675 )

cProfile.run('Map.Perlin.generate2D( 8192, 32, 128, 88005553535)')
#Render.Render.drawHeightMap(MapToDraw)

#print( "Map generated!" )

#while True:
    #pass
    #Render.Render.Window.flip()