import pygame, math


LINE_WIDTH = 3


def to_dict(x, y, z):
    return {
        "x": x,
        "y": y,
        "z": z
    }


def screen(p, sw, sh):
    # translates point so that (0, 0) is center
    # currently -1..1, should be 0..w/h
    # -1..1 => 0..2 => 0..1 => 0..w/h
    return pygame.Vector2(
        (p.x + 1) / 2 * sw,
        (p.y + 1) / 2 * sh
    )


def project(p):
    # takes (x, y, z) and turns it into (x', y')
    # 3d => 2d
    return pygame.Vector2(
        p.x / p.z,
        p.y / p.z
    )


def get_intersection(p1, p2):
    clip_z = 1
    t = (clip_z - p1[2]) / (p2[2] - p1[2])
    return pygame.Vector3(
        p1[0] + t * (p2[0] - p1[0]),
        p1[1] + t * (p2[1] - p1[1]),
        clip_z
    )


def rotate(v: pygame.Vector3, rotation: pygame.Vector3):
    v2 = v.rotate_rad(-rotation.y, pygame.Vector3(0, 1, 0))   # y-axis rotation
    v3 = v2.rotate_rad(rotation.x, pygame.Vector3(1, 0, 0))   # x-axis rotation
    return v3


def translate(v: pygame.Vector3, translation: pygame.Vector3, rotation: pygame.Vector3):
    return rotate(v + translation, rotation)



def render(display_size: tuple, objs: list, col, rotation: dict, position):
    """
    Object: {
        pos: pygame.Vector3(x, y, z),
        size: pygame.Vector3(w, h, l)
    }
    """
    
    display = pygame.Surface(display_size)
    sw, sh = display_size[0], display_size[1]

    # create vertices and faces
    vs = []   # vertices
    fs = []   # faces
    for i, obj in enumerate(objs):
        j = i*8

        x, y, z = obj.pos.x, -(obj.pos.y - 1), obj.pos.z
        w, h, l = obj.size.x/2, obj.size.y/2, obj.size.z/2

        vs.extend([
            pygame.Vector3(x-w, y+h, z+l),
            pygame.Vector3(x+w, y+h, z+l),
            pygame.Vector3(x+w, y-h, z+l),
            pygame.Vector3(x-w, y-h, z+l),
            pygame.Vector3(x-w, y+h, z-l),
            pygame.Vector3(x+w, y+h, z-l),
            pygame.Vector3(x+w, y-h, z-l),
            pygame.Vector3(x-w, y-h, z-l)
        ])

        fs.extend([
            [j+0, j+1, j+2, j+3],
            [j+4, j+5, j+6, j+7],
            [j+0, j+4],
            [j+1, j+5],
            [j+2, j+6],
            [j+3, j+7],
        ])

    # rotate all vertices
    for i, v in enumerate(vs):
        vs[i] = translate(v, position, rotation)
    
    # draw faces
    for f in fs:
        for i in range(0, len(f), 1):
            p1 = vs[f[i]]
            p2 = vs[f[(i+1)%len(f)]]

            if p1.z <= 0 and p2.z <= 0:
                continue
            
            if p1.z <= 0 or p2.z <= 0:
                pi = get_intersection((p1.x, p1.y, p1.z), (p2.x, p2.y, p2.z))
                if p1.z > 0 and p2.z <= 0: p2 = pi
                if p1.z <= 0 and p2.z > 0: p1 = pi
            
            pygame.draw.line(
                display,
                col, 
                screen(project(p1), sw, sh),
                screen(project(p2), sw, sh),
                LINE_WIDTH
            )

    return display