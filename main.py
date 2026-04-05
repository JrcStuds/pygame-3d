import pygame, math
from renderer import render
from object import Object


DISPLAY_SIZE = (800, 800)
COLOUR = "green"
SHOW_FLOOR = False
speed = 2


pygame.init()
display = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()
dt = 0
pygame.mouse.set_relative_mode(True)


fps = "0"
font = pygame.font.SysFont('Arial', 20)
fps_surface = font.render(fps, True, "white")

stone_tex = pygame.image.load('textures/stone.png').convert()
grass_tex = pygame.image.load('textures/grass.png').convert()
dirt_tex = pygame.image.load('textures/dirt.png').convert()
oak_log_top_tex = pygame.image.load('textures/oak_log_top.png').convert()
oak_log_side_tex = pygame.image.load('textures/oak_log_side.png').convert()

objs = [
    Object(0, 0, 4, 1, 1, 1, [stone_tex]),
    Object(1, 1, 4, 1, 1, 1, [oak_log_side_tex, oak_log_top_tex], [0,0,0,0,1,1]),
    Object(0, 1, 4, 1, 1, 1, [oak_log_side_tex, oak_log_top_tex], [0,0,0,0,1,1]),
    Object(-1, 0, 4, 1, 1, 1, [stone_tex]),
    Object(-1, 1, 4, 1, 1, 1, [dirt_tex]),
    Object(-1, 2, 4, 1, 1, 1, [stone_tex]),
    Object(-1, 3, 4, 1, 1, 1),
    Object(-1, 4, 4, 1, 1, 1, [stone_tex]),
]

if SHOW_FLOOR:
    for i in range(5):
        for j in range(5):
            objs.append(Object(i-2, 0, j-2, 1, 0, 1))
            objs.append(Object(i-2, 2, j-2, 1, 0, 1))


movement = {
    "forward": [pygame.Vector3(0, 0, -1), False],
    "backward": [pygame.Vector3(0, 0, 1), False],
    "left": [pygame.Vector3(1, 0, 0), False],
    "right": [pygame.Vector3(-1, 0, 0), False],
    "up": [pygame.Vector3(0, 1, 0), False],
    "down": [pygame.Vector3(0, -1, 0), False],
}



rotation = pygame.Vector3(0, 0, 0)
position = pygame.Vector3(0, 1, 0)



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

                case pygame.K_SPACE: movement["up"][1] = True
                case pygame.K_LSHIFT: movement["down"][1] = True
                case pygame.K_w: movement["forward"][1] = True
                case pygame.K_a: movement["left"][1] = True
                case pygame.K_s: movement["backward"][1] = True
                case pygame.K_d: movement["right"][1] = True

                case pygame.K_LCTRL: speed = 4
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_SPACE: movement["up"][1] = False
                case pygame.K_LSHIFT: movement["down"][1] = False
                case pygame.K_w: movement["forward"][1] = False
                case pygame.K_a: movement["left"][1] = False
                case pygame.K_s: movement["backward"][1] = False
                case pygame.K_d: movement["right"][1] = False

                case pygame.K_LCTRL: speed = 2
        
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_relative_mode() == False:
                continue

            rotation.y += event.rel[0] * 0.5 * dt
            rotation.x += event.rel[1] * 0.5 * dt
            
            if rotation.x > 0.5*math.pi: rotation.x = 0.5*math.pi
            if rotation.x < -0.5*math.pi: rotation.x = -0.5*math.pi

            if rotation.y > 2*math.pi: rotation.y = 0
            if rotation.y < 0: rotation.y = 2*math.pi
        

    display.fill("black")
    display.blit(render(DISPLAY_SIZE, objs, COLOUR, rotation, position))

    fps_surface = font.render(f"FPS: {fps}", True, "white")
    pos_surface = font.render(f"(x: {str(position.x)[0:5]}, y: {str(position.y)[0:5]}, z: {str(position.z)[0:5]})", True, "white")
    rotation_surface = font.render(f"(x: {str(rotation.x)[0:5]}, y: {str(rotation.y)[0:5]}, z: {str(rotation.z)[0:5]})", True, "white")
    display.blit(fps_surface, (0, 0))
    display.blit(pos_surface, (0, 30))
    display.blit(rotation_surface, (0, 60))


    movement_vector = pygame.Vector3(0, 0, 0)
    for key in movement.keys():
        if movement[key][1]:
            movement_vector += movement[key][0]
    if movement_vector:
        movement_vector = movement_vector.normalize()
        movement_vector.rotate_rad_ip(rotation.y, pygame.Vector3(0, 1, 0))
        movement_vector *= speed * dt
        position += movement_vector


    pygame.display.flip()
    dt = clock.tick(60) / 1000
    fps = str(math.floor(1/dt))


pygame.quit()