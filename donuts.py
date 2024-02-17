from typing import Any
import pygame
from os import path

IMG_DIR = "images/"
VELOCITY_UNIT = 0.5
PLAYER_DIMENSIONS = (64, 64)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.velocity = (0, 0)

        original_image = pygame.image.load(
            path.join(IMG_DIR, "donut.png")
        ).convert_alpha()
        image = pygame.transform.scale(original_image, PLAYER_DIMENSIONS)
        self.image = image

        self.rect = self.image.get_rect()

    def update(self):
        if (
            self.position[0] == 0
            or self.position[0] == screen.get_width() - PLAYER_DIMENSIONS[0]
        ):
            self.velocity = (-self.velocity[0], self.velocity[1])

        if (
            self.position[1] == 0
            or self.position[1] == screen.get_height() - PLAYER_DIMENSIONS[1]
        ):
            self.velocity = (self.velocity[0], -self.velocity[1])

        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )

    def move_left(self):
        self.velocity = (-VELOCITY_UNIT, self.velocity[1])

    def move_right(self):
        self.velocity = (VELOCITY_UNIT, self.velocity[1])

    def move_up(self):
        self.velocity = (self.velocity[0], -VELOCITY_UNIT)

    def move_down(self):
        self.velocity = (self.velocity[0], +VELOCITY_UNIT)

    def draw(self, surface):
        surface.blit(self.image, self.position)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill("gray")
running = True

player = Player()
player_list = pygame.sprite.Group()
player_list.add(player)
player.draw(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_UP:
                player.move_up()
            elif event.key == pygame.K_DOWN:
                player.move_down()

    player.update()
    player.draw(screen)

    pygame.display.update()
    screen.fill("gray")

pygame.quit()
