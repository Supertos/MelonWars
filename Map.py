import numpy as np
import math

import cProfile


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

                    out[x][y] = lerped12 + ((y - closest_y) / frequency) * (lerped34 - lerped12)
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
        hgt_a = Perlin.generate2D( size, 32, 128, seed)
        print( "Generating mountains completed!")
        hgt_b = Perlin.generate2D( size, 128, 64, seed+1)
        print( "Generating hills completed!")
        hgt_c = Perlin.generate2D( size, 64, 32, seed+2)
        print( "Generating small hills completed!")
        hgt_e = Perlin.generate2D( size, 8, 2, seed+4)
        print( "Generating minor obstacles completed!")

        self.Height = Perlin.addLists( hgt_a, Perlin.addLists( hgt_b,  Perlin.addLists( hgt_c, hgt_e, 255 ), 255), 255)

    def getSize(self):
        return self.Size
