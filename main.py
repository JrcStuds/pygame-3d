import pygame, math
from renderer import render


DISPLAY_SIZE = (800, 800)
COLOUR = "green"
SHOW_FLOOR = False


pygame.init()
display = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()
dt = 0
pygame.mouse.set_relative_mode(True)


fps = "0"
font = pygame.font.SysFont('Arial', 20)
fps_surface = font.render(fps, True, "white")


def new_obj(x, y, z, w, h, l):
    return {
        "x": x,
        "y": y,
        "z": z,
        "w": w,
        "h": h,
        "l": l
    }

objs = [
    new_obj(0, 4, 0, 2, 0, 2),
    new_obj(0, -2, 0, 2, 0, 2),
    new_obj(0, 1, 3, 2, 2, 0),
    new_obj(0, 1, -3, 2, 2, 0),
    new_obj(3, 1, 0, 0, 2, 2),
    new_obj(-3, 1, 0, 0, 2, 2),
]

if SHOW_FLOOR:
    objs.append(new_obj(0, 0, 0, 5, 0, 5))



rotation = {
    "x": 0,
    "y": 0
}



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    if pygame.mouse.get_relative_mode() == True:
                        pygame.mouse.set_relative_mode(False)
                    else:
                        pygame.mouse.set_relative_mode(True)
        
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_relative_mode() == False:
                continue

            rotation["y"] += event.rel[0] * 0.5 * dt
            rotation["x"] += event.rel[1] * 0.5 * dt
            
            if rotation["x"] > 0.5*math.pi: rotation["x"] = 0.5*math.pi
            if rotation["x"] < -0.5*math.pi: rotation["x"] = -0.5*math.pi
        

    display.fill("black")
    display.blit(render(DISPLAY_SIZE, objs, COLOUR, rotation))

    fps_surface = font.render(fps, True, "white")
    display.blit(fps_surface, (0, 0))


    pygame.display.flip()
    dt = clock.tick(60) / 1000
    fps = str(math.floor(1/dt))


pygame.quit()