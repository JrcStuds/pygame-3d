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
    rot = pygame.Vector3(
        -1 if rotation.y > math.pi else 1,
        -1 if rotation.x > 0 else 1,
        -1 if rotation.y > 0.5*math.pi and rotation.y < 1.5*math.pi else 1
    )
    to_cull = []

    # cull touching faces
    for i, f1 in enumerate(fs):
        for j, f2 in enumerate(fs):
            if f1["centre"] == f2["centre"] and i != j:
                to_cull.append(i)
    to_cull = cull(to_cull, fs)

    # cull faces facing away from camera
    for i, f in enumerate(fs):
        a = vs[f["pixel_fs"][15]["vs"][1]]
        b = vs[f["pixel_fs"][0]["vs"][0]]
        c = vs[f["pixel_fs"][255]["vs"][3]]
        ab = b - a
        ac = c - a
        n = ab.cross(ac)
        n.normalize_ip()
        if n.z > 0:
            to_cull.append(i)
    to_cull = cull(to_cull, fs)

    return fs



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
        if obj.type == "wireframe":
            for v in obj.vs:
                vs.append(pygame.Vector3(
                    v.x,
                    v.y * -1,
                    v.z
                ))
            
            for f in obj.fs:
                fs.append([])
                for v in f:
                    fs[-1].append(v + i*8)

        if obj.type == "textured":
            for v in obj.vs:
                vs.append(pygame.Vector3(
                    v.x,
                    v.y * -1,
                    v.z
                ))

            for f in obj.fs:   # 256 pixel_vs per f
                fs.append({
                    "orientation": f["orientation"],
                    "centre": transform([f["centre"]], position, rotation)[0],
                    "pixel_fs": [
                        {
                            "vs": [
                                v + i*6*17*17 for v in pixel_f["vs"]
                            ],
                            "col": pixel_f["col"]
                        } for pixel_f in f["pixel_fs"]
                    ]
                })

    # rotate all vertices
    vs = transform(vs, position, rotation)

    cull_faces(fs, vs, position, rotation)
    
    # sort pixel distances
    fs2 = []
    for f in fs:
        for pixel_f in f["pixel_fs"]:
            v_indices = pixel_f["vs"]
            avg_z = sum(vs[v].z for v in v_indices) / len(v_indices)
            if avg_z > 0.1:
                fs2.append({
                    "vs": v_indices[:],
                    "col": pixel_f["col"],
                    "depth": avg_z
                })
    
    fs2.sort(key=lambda f: f["depth"], reverse=True)
    

    # draw faces
    for j, f in enumerate(fs):
        if type(f) == list:
            for i in range(len(f)):
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

        elif type(f) == dict:
            for f in fs2:
                vs2 = []
                for v in f["vs"]:
                    vs2.append(screen(project(vs[v]), sw, sh))
                pygame.draw.polygon(display, f["col"], vs2)
    return display