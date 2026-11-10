from pico2d import *

import game_world
import game_framework

from boy import Boy
from grass import Grass
from bird import Bird


boy = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            return

        else:
            boy.handle_event(event)


def init():
    global boy

    grass = Grass()
    game_world.add_oject(grass, 0)

    boy = Boy()
    game_world.add_oject(boy, 1)

    bird = Bird(800, 400)
    game_world.add_oject(bird, 1)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy

    game_world.clear()
    boy = None


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()