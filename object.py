import pygame


class Object():
    def __init__(self, x, y, z, w, h, l):
        self.pos = pygame.Vector3(x, y, z)
        self.size = pygame.Vector3(w, h, l)