import uuid
from collections import defaultdict
from typing import Callable

import pygame
from termdraw import Screen, FULL_CHAR
from game import Bird, Pipe, GameState
from abc import ABC, abstractmethod


class Drawer(ABC):
    @abstractmethod
    def draw_state(self, state: GameState):
        ...


class CursesDrawer(Drawer):
    def __init__(self, screen: Screen):
        self.screen = screen

    def draw_state(self, state: GameState):
        for bird in state.birds:
            self.screen.add_pixel((10, round(bird.y)), 1)


class PygameDrawer(Drawer):
    def __init__(self, inp_callback: Callable = None):
        successes, failures = pygame.init()
        print(
            "Initializing pygame: {0} successes and {1} failures.".format(
                successes, failures
            )
        )

        self.screen = pygame.display.set_mode((720, 720))
        self.clock = pygame.time.Clock()
        self.FPS = 240
        self.bird_surfs: dict[uuid.UUID, pygame.Surface] = defaultdict(
            self.bird_surf_factory
        )
        self.pipe_surfs: dict[uuid.UUID, pygame.Surface] = defaultdict(
            self.pipe_surf_factory
        )
        self.inp_callback = inp_callback or (lambda x: None)
        self.score = 0
        self.font = pygame.font.SysFont(None, 24)

    def draw_state(self, state: GameState):
        delta = self.clock.tick(self.FPS)
        self.score += 1
        for event in pygame.event.get():
            # Check for exit
            if event.type == pygame.KEYDOWN:
                self.inp_callback(pygame.key.name(event.key))
            if event.type == pygame.QUIT:
                quit()

        self.screen.fill((0, 0, 0))
        for bird in state.birds:
            if bird.dead:
                continue

            pygame.draw.rect(
                self.screen, (255, 255, 255), pygame.Rect(200 - 16, bird.y - 16, 32, 32)
            )
            self.debug_dot(
                200,
                bird.y,
            )

        for pipe in state.pipes:
            surf = self.pipe_surfs[pipe.id]
            rect_bot = pygame.Rect(
                pipe.x - state.birds[0].x - 16 + 200,
                pipe.y - 16 + pipe.opening_size / 2,
                100,
                1000,
            )
            rect_up = pygame.Rect(
                pipe.x - state.birds[0].x - 16 + 200,
                -1000 + pipe.y - 16 - pipe.opening_size / 2,
                100,
                1000,
            )
            self.screen.blit(surf, rect_up)
            self.screen.blit(surf, rect_bot)

        score_img = self.font.render(f"score:{state.score}", True, (0, 255, 0))
        gensize_img = self.font.render(
            f"gen size:{len(state.birds)}", True, (0, 255, 0)
        )
        self.screen.blit(score_img, (20, 20))
        self.screen.blit(gensize_img, (20, 40))

        pygame.display.update()

    def bird_surf_factory(self):
        surf = pygame.Surface((32, 32))
        surf.fill((255, 255, 255))
        return surf

    def pipe_surf_factory(self):
        surf = pygame.Surface((32, 1000))
        surf.fill((255, 255, 255))
        return surf

    def debug_dot(self, x, y):
        surf = pygame.Surface((6, 6))
        surf.fill((255, 0, 0))
        rect = pygame.Rect(x - 3, y - 3, 10, 10)
        self.screen.blit(surf, rect)
