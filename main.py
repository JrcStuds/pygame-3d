import pygame, math
from renderer import render
from object import Object


DISPLAY_SIZE = (800, 800)
COLOUR = "green"
SHOW_FLOOR = True
SPEED = 1


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
    Object(0, 1, 3, 1, 1, 0),
    Object(0, 1, -3, 1, 1, 0),
    Object(3, 1, 0, 0, 1, 1),
    Object(-3, 1, 0, 0, 1, 1),
]

if SHOW_FLOOR:
    for i in range(5):
        for j in range(5):
            objs.append(Object(i-2, 0, j-2, 1, 0, 1))
            objs.append(Object(i-2, 2, j-2, 1, 0, 1))


keys = {
    "forward": False,
    "backward": False,
    "left": False,
    "right": False,
    "up": False,
    "down": False
}
movement = {
    "forward": pygame.Vector3(0, 0, -1),
    "backward": pygame.Vector3(0, 0, 1),
    "left": pygame.Vector3(1, 0, 0),
    "right": pygame.Vector3(-1, 0, 0),
    "up": pygame.Vector3(0, 1, 0),
    "down": pygame.Vector3(0, -1, 0),
}



rotation = pygame.Vector3(0, 0, 0)
position = pygame.Vector3(0, 0, 0)



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

                case pygame.K_SPACE: keys["up"] = True
                case pygame.K_LSHIFT: keys["down"] = True
                case pygame.K_w: keys["forward"] = True
                case pygame.K_a: keys["left"] = True
                case pygame.K_s: keys["backward"] = True
                case pygame.K_d: keys["right"] = True
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_SPACE: keys["up"] = False
                case pygame.K_LSHIFT: keys["down"] = False
                case pygame.K_w: keys["forward"] = False
                case pygame.K_a: keys["left"] = False
                case pygame.K_s: keys["backward"] = False
                case pygame.K_d: keys["right"] = False
        
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_relative_mode() == False:
                continue

            rotation.y += event.rel[0] * 0.5 * dt
            rotation.x += event.rel[1] * 0.5 * dt
            
            if rotation.x > 0.5*math.pi: rotation.x = 0.5*math.pi
            if rotation.x < -0.5*math.pi: rotation.x = -0.5*math.pi
        

    display.fill("black")
    display.blit(render(DISPLAY_SIZE, objs, COLOUR, rotation, position))

    fps_surface = font.render(fps, True, "white")
    display.blit(fps_surface, (0, 0))


    movement_vector = pygame.Vector3(0, 0, 0)
    for key in keys.keys():
        if keys[key]:
            movement_vector += movement[key]
    if movement_vector:
        movement_vector = movement_vector.normalize()
        movement_vector.rotate_rad_ip(rotation.y, pygame.Vector3(0, 1, 0))
        movement_vector *= SPEED * dt
        position += movement_vector


    pygame.display.flip()
    dt = clock.tick(60) / 1000
    fps = str(math.floor(1/dt))


pygame.quit()