import pygame, math


LINE_WIDTH = 3


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


def translate(v: pygame.Vector3, translation: pygame.Vector3):
    return v + translation


def transform(vs: list, translation: pygame.Vector3, rotation: pygame.Vector3):
    vs2 = []
    for v in vs:
        v2 = translate(v, translation)
        v2 = rotate(v2, rotation)
        vs2.append(v2)
    return vs2


def cull(to_cull: list, fs: list):
    to_cull.sort(reverse=True)
    for i in to_cull:
        fs.pop(i)
    return []


def cull_faces(fs: list, vs:list, position: pygame.Vector3, rotation: pygame.Vector3):
    to_cull = []
    seen_faces = {}

    for i, f in enumerate(fs):
        # cull faces facing away from camera
        a = vs[f[15]["vs"][1]]
        b = vs[f[0]["vs"][0]]
        c = vs[f[255]["vs"][3]]
        n = (b - a).cross(c - a)
        if n.dot(a) > 0:
            to_cull.append(i)

        # cull touching faces
        """
        centre = vs[f[127]["vs"][2]]
        key = (centre.x, centre.y, centre.z)
        if key in seen_faces.keys():
            to_cull.append(i)
            to_cull.append(seen_faces[key])
        else:
            seen_faces[key] = i
        """

    to_cull = list(set(to_cull))
    cull(to_cull, fs)

    return fs



def render(display_size: tuple, objs: list, col, rotation: dict, position):
    display = pygame.Surface(display_size)
    sw, sh = display_size[0], display_size[1]

    vs = []   # vertices
    fs = []   # faces

    for i, obj in enumerate(objs):
        for v in obj.vs:
            vs.append(pygame.Vector3(
                v.x,
                v.y * -1,
                v.z
            ))

        index_offset = i*6*17*17
        fs.extend([
            [
                {
                    "vs": [
                        index_offset + v for v in pixel_f["vs"]
                    ],
                    "col": pixel_f["col"]
                } for pixel_f in f
            ] for f in obj.fs
        ])

    # rotate all vertices
    vs = transform(vs, position, rotation)

    cull_faces(fs, vs, position, rotation)
    
    # sort pixel distances
    fs2 = []
    for f in fs:
        for pixel_f in f:
            pixel_vs = pixel_f["vs"]
            avg_z = sum(vs[v].z for v in pixel_vs) / len(pixel_vs)
            if avg_z > 0.1:
                fs2.append({
                    "vs": pixel_vs,
                    "col": pixel_f["col"],
                    "depth": avg_z
                })
    fs2.sort(key=lambda f: f["depth"], reverse=True)
    

    # draw faces / pixels
    for f in fs2:
        vs2 = []
        for v in f["vs"]:
            vs2.append(screen(project(vs[v]), sw, sh))
        pygame.draw.polygon(display, f["col"], vs2)
            
    return display



"""

Object: {
    pos: pygame.Vector3(x, y, z),
    size: pygame.Vector3(w, h, l),

}

"""