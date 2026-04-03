import pygame, math


# (x, y, z)
# x' = x/z
# y' = y/z


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
primary_col = "green"


pygame.init()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0


def obj(x, y, z):
    # turns 3 values into a dict of (x, y, z)
    return {
        "x": x,
        "y": y,
        "z": z
    }


def point(p):
    # draws point on the screen
    r = 5
    pygame.draw.circle(display, primary_col, (p["x"], p["y"]), r)


def line(p1, p2):
    # draws line from p1 to p2
    w = 3
    pygame.draw.line(display, primary_col, (p1["x"], p1["y"]), (p2["x"], p2["y"]), w)


def screen(p):
    # translates point so that (0, 0) is center
    # currently -1..1, should be 0..w/h
    # -1..1 => 0..2 => 0..1 => 0..w/h
    return {
        "x": (p["x"] + 1) / 2 * SCREEN_WIDTH,
        "y": (p["y"] + 1) / 2 * SCREEN_HEIGHT
    }


def project(p):
    # takes (x, y, z) and turns it into (x', y')
    return {
        "x": p["x"] / p["z"],
        "y": p["y"] / p["z"]
    }


def translate_z(p, dz):
    return {
        "x": p["x"],
        "y": p["y"],
        "z": p["z"] + dz,
    }


def rotate_zx(p, angle):
    # x' = xcos(theta) - ysin(theta)
    # y' = xsin(theta) + ycos(theta)
    return {
        "x": p["x"]*math.cos(angle) - p["z"]*math.sin(angle),
        "y": p["y"],
        "z": p["x"]*math.sin(angle) + p["z"]*math.cos(angle),
    }


vs = [   # vertices
    {"x":  0.5, "y":  0.5, "z":  0.5},
    {"x": -0.5, "y":  0.5, "z":  0.5},
    {"x": -0.5, "y": -0.5, "z":  0.5},
    {"x":  0.5, "y": -0.5, "z":  0.5},

    {"x":  0.5, "y":  0.5, "z": -0.5},
    {"x": -0.5, "y":  0.5, "z": -0.5},
    {"x": -0.5, "y": -0.5, "z": -0.5},
    {"x":  0.5, "y": -0.5, "z": -0.5},
]

fs = [   # faces
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
]


dz = 1
angle = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    display.fill("black")

    dz += 1 * dt
    angle += math.pi * dt

    for v in vs:
        point(screen(project(translate_z(rotate_zx(v, angle), dz))))

    for f in fs:
        for i in range(0, len(f), 1):
            p1 = vs[f[i]]
            p2 = vs[f[(i + 1) % len(f)]]
            line(
                screen(project(translate_z(rotate_zx(p1, angle), dz))),
                screen(project(translate_z(rotate_zx(p2, angle), dz))),
            )


    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()