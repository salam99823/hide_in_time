from enum import Enum

import pygame
from pygame.locals import RESIZABLE
from pygame.time import Clock

from .scene import Scene


class App:
    flags = RESIZABLE
    fps: int = 0
    running: bool = False
    clock: Clock
    state: Enum
    screen: pygame.Surface
    scenes: dict[Enum, Scene]

    def __init__(
        self,
        scenes: dict,
        state: Enum,
    ) -> None:
        pygame.init()
        self.scenes = scenes
        self.state = state

    def run(self):
        self.screen = pygame.display.set_mode((500, 200), self.flags)
        self.running = True
        self.clock = Clock()
        for scene in self.scenes.values():
            scene.set_screen(self.screen)
        while self.running:
            scene = self.scenes[self.state]
            scene.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False
                    case pygame.VIDEORESIZE | pygame.VIDEOEXPOSE:
                        scene.set_screen(self.screen)
                        scene.draw()
                        pygame.display.flip()
                    case _:
                        yield event
                        scene.handle_event(event)
            self.clock.tick(self.fps)
        pygame.quit()
