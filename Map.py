import numpy as np
import math


class Perlin:
    @staticmethod
    def interpolate( a, b, lerp ):
        return int( a + (b - a) * lerp )

    @staticmethod
    def sosi_hui_gvido( lst, x, y ):
        if len(lst) <= x: return 0
        if len(lst[x]) <= y: return 0
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

                    x1 = Perlin.sosi_hui_gvido(out, closest_x, closest_y)
                    x2 = Perlin.sosi_hui_gvido(out, closest_x + frequency, closest_y)
                    x3 = Perlin.sosi_hui_gvido(out, closest_x, closest_y + frequency)
                    x4 = Perlin.sosi_hui_gvido(out, closest_x + frequency, closest_y + frequency)

                    lerp = abs( (x//frequency*frequency+frequency - x )/frequency )
                    interpolated_x1x2 = Perlin.interpolate(x1, x2, lerp )
                    interpolated_x3x4 = Perlin.interpolate(x3, x4, lerp )
                    lerp = abs( (y//frequency*frequency+frequency - y )/frequency )

                    interpolated_final = Perlin.interpolate(interpolated_x1x2, interpolated_x3x4, lerp )
                    out[x][y] = interpolated_final
        return out

    @staticmethod
    def addLists(a,b, max_val):
        out = []
        for x in range(len(a)):
            out.append([])
            for y in range(len(a)):
                out[x].append( min(max_val,a[x][y] + b[x][y]) )
        return out

class Map:

    def __init__(self, size, seed):
        global MAP
        MAP = self

        self.Size = size
        self.Seed = seed
        hgt_a = Perlin.generate2D( size, 32, 256, seed)
        print( "Generating mountains completed!")
        #hgt_b = Perlin.generate2D( size, 128, 128, seed+1)
        print( "Generating hills completed!")
        #hgt_c = Perlin.generate2D( size, 64, 64, seed+2)
        print( "Generating small hills completed!")
        #hgt_e = Perlin.generate2D( size, 8, 2, seed+4)
        print( "Generating minor obstacles completed!")

        self.Height = hgt_a #Perlin.addLists( hgt_a, Perlin.addLists( hgt_b,  Perlin.addLists( hgt_c, hgt_e, 256 ), 256), 256)

    def getSize(self):
        return self.Size
