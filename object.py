import pygame


"""
    Object.fs = [
        {
            "orientation": pygame.Vector3(),
            "centre": pygame.Vector3(),
            "pixel_fs": [
                {"vs": [v0, v1, v2, v3], "col": str},
                ...
            ]
        },
        ...
    ]
"""


class Object():
    def __init__(self, x, y, z, w, h, l, textures=[], texture_mapping=[0,0,0,0,0,0]):
        self.pos = pygame.Vector3(x, y, z)
        self.size = pygame.Vector3(w, h, l)
        self.type = "textured" if textures else "wireframe"

        self.vs = [
            pygame.Vector3(x-w/2, y+h/2, z+l/2),
            pygame.Vector3(x+w/2, y+h/2, z+l/2),
            pygame.Vector3(x+w/2, y-h/2, z+l/2),
            pygame.Vector3(x-w/2, y-h/2, z+l/2),
            pygame.Vector3(x-w/2, y+h/2, z-l/2),
            pygame.Vector3(x+w/2, y+h/2, z-l/2),
            pygame.Vector3(x+w/2, y-h/2, z-l/2),
            pygame.Vector3(x-w/2, y-h/2, z-l/2)
        ]
        self.fs = [
            [[1, 0, 3, 2], pygame.Vector3( 0,  0,  1)],   #  z
            [[4, 5, 6, 7], pygame.Vector3( 0,  0, -1)],   # -z
            [[0, 4, 7, 3], pygame.Vector3(-1,  0,  0)],   # -x
            [[5, 1, 2, 6], pygame.Vector3( 1,  0,  0)],   #  x
            [[0, 1, 5, 4], pygame.Vector3( 0,  1,  0)],   #  y
            [[7, 6, 2, 3], pygame.Vector3( 0, -1,  0)]    # -y
        ]

        if self.type == "textured": self.create_texture(textures, texture_mapping)


    
    def create_texture(self, textures: list, texture_mapping: list):
        vs2, fs2 = [], []

        for i, f in enumerate(self.fs):
            origin = self.vs[f[0][0]]   # position vectors
            centre = (self.vs[f[0][0]] + self.vs[f[0][2]]) / 2
            unit_right = (self.vs[f[0][1]] - self.vs[f[0][0]]) / 16   # movement vectors
            unit_down = (self.vs[f[0][2]] - self.vs[f[0][1]]) / 16

            pixel_vs, pixel_fs = [], []

            for j in range(17):
                for k in range(17):
                    pixel_vs.append(origin + k*unit_right + j*unit_down)
            
            vs2.extend(pixel_vs)
            
            for j in range(16):
                for k in range(16):
                    pixel = textures[texture_mapping[i]].subsurface(pygame.Rect(k, j, 1, 1))
                    col = pixel.get_at((0, 0)).hex
                    
                    # len(obj.vs) = 6x17x17 or 6x289 (6 f * 16x16 pixel_fs (top-left and bottom-right corners))
                    # in obj there are 6 fs, in f there is 16x16 pixel_fs, in each pixel_f["vs"] there are 4 vs pointers
                    # in the pixel_f["vs"], relative j (x) by k (y), add i (fs) * 256 (pixel_fs per f)
                    pixel_fs.append({
                        "vs": [
                            (j*17 + k) + i*17*17,
                            (j*17 + k+1) + i*17*17,
                            ((j+1)*17 + k+1) + i*17*17,
                            ((j+1)*17 + k) + i*17*17,
                        ],
                        "col": col
                    })
            
            fs2.append({
                "orientation": f[1],
                "centre": centre,
                "pixel_fs": pixel_fs
            })

        self.vs = vs2
        self.fs = fs2