
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
