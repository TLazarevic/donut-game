import random
from typing import Any
import pygame
from os import path

IMG_DIR = "images/"
VELOCITY_UNIT = 0.5
FIGURE_DIMENSIONS = (64, 64)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.velocity = (0, 0)

        original_image = pygame.image.load(
            path.join(IMG_DIR, "donut.png")
        ).convert_alpha()
        image = pygame.transform.scale(original_image, FIGURE_DIMENSIONS)
        self.image = image

        self.rect = self.image.get_rect()

    def update(self):
        if (
            self.position[0] == 1
            or self.position[0] == screen.get_width() - FIGURE_DIMENSIONS[0]
        ):
            self.velocity = (-self.velocity[0], self.velocity[1])

        if (
            self.position[1] == 1
            or self.position[1] == screen.get_height() - FIGURE_DIMENSIONS[1]
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


class Enemy(
    pygame.sprite.Sprite,
):
    def __init__(self, groups):
        super().__init__(groups)
        self.position = pygame.Vector2(10, 10)
        velocities = [(1, 1), (0, 1), (1, 0)]
        self.velocity = velocities[random.randint(0, 2)]

        original_image = pygame.image.load(
            path.join(IMG_DIR, "broccoli.png")
        ).convert_alpha()
        image = pygame.transform.scale(original_image, FIGURE_DIMENSIONS)
        self.image = image

        self.rect = self.image.get_rect()

    def update(self):
        if (
            self.position[0] == 1
            or self.position[0] == screen.get_width() - FIGURE_DIMENSIONS[0]
        ):
            self.velocity = (-self.velocity[0], self.velocity[1])

        if (
            self.position[1] == 1
            or self.position[1] == screen.get_height() - FIGURE_DIMENSIONS[1]
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


class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, ds):
        for spr in self.sprites():
            spr.draw(ds)

    def update(self):
        for spr in self.sprites():
            spr.update()


def intersects(first, second):
    def _get_bounds(player):
        top_right_x = player.position[0] + FIGURE_DIMENSIONS[0] / 2
        top_right_y = player.position[1] + FIGURE_DIMENSIONS[1] / 2
        bottom_left_x = player.position[0] - FIGURE_DIMENSIONS[0] / 2
        bottom_left_y = player.position[1] - FIGURE_DIMENSIONS[1] / 2

        return top_right_x, top_right_y, bottom_left_x, bottom_left_y

    (
        first_top_right_x,
        first_top_right_y,
        first_bottom_left_x,
        first_bottom_left_y,
    ) = _get_bounds(first)
    (
        second_top_right_x,
        second_top_right_y,
        second_bottom_left_x,
        second_bottom_left_y,
    ) = _get_bounds(second)

    return not (
        first_top_right_x < second_bottom_left_x
        or first_bottom_left_x > second_top_right_x
        or first_top_right_y < second_bottom_left_y
        or first_bottom_left_y > second_top_right_y
    )


pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill("gray")
running = True

clock = pygame.time.Clock()

player = Player()
enemy_group = EnemyGroup()
enemy = Enemy(enemy_group)
enemy_group.add(enemy)

while running:
    time_elapsed = pygame.time.get_ticks()
    font = pygame.font.SysFont("Arial", 18)
    text = font.render("Score: {}".format(time_elapsed // 1000), True, (0, 0, 0))
    screen.blit(text, (0, 0))

    if time_elapsed % 10000 == 0:
        new_enemy = Enemy(enemy_group)

    for enemy in enemy_group.sprites():
        if intersects(player, enemy):
            running = False

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
    enemy_group.update()
    player.draw(screen)
    enemy_group.draw(screen)

    clock.tick()
    pygame.display.update()
    screen.fill("gray")


pygame.quit()
