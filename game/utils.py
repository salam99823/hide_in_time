from pathlib import Path

import pygame

ASSETS_DIR = Path("./assets/").absolute()
IMAGES_DIR = ASSETS_DIR.joinpath("images/")

_NEXT_EVENT = pygame.USEREVENT + 1


def load_image(name: str):
    for filename in IMAGES_DIR.glob(f"{name}.*"):
        if filename.name.endswith(".png"):
            return pygame.load_image(filename).convert_alpha()
        else:
            return pygame.load_image(filename).convert()


def new_event_type() -> int:
    global _NEXT_EVENT
    current = _NEXT_EVENT
    _NEXT_EVENT += 1
    return current
