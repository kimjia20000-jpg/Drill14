from pico2d import *

import game_world
import game_framework

from boy import Boy
from grass import Grass
from bird import Bird, FRAME_COUNT


BIRD_COUNT = 10

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

    # 화면 가로 방향으로 새 10마리를 나누어 배치한다.
    spacing = get_canvas_width() / (BIRD_COUNT + 1)

    for i in range(BIRD_COUNT):
        x = spacing * (i + 1)

        # 세 가지 높이를 번갈아 사용한다.
        y = 300 + (i % 3) * 100

        # 오른쪽과 왼쪽 방향을 번갈아 지정한다.
        direction = 1 if i % 2 == 0 else -1

        # 날갯짓 시작 시점을 한 사이클 안에서 분산한다.
        frame = i * FRAME_COUNT / BIRD_COUNT

        bird = Bird(
            x=x,
            y=y,
            direction=direction,
            frame=frame
        )

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