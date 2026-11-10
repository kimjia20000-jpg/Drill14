from pico2d import load_image, get_canvas_width

import game_framework


FRAME_COLUMNS = 5
FRAME_ROWS = 3
FRAME_COUNT = 14

# 1초에 14프레임: 날갯짓 한 사이클
FRAMES_PER_SECOND = 14.0

# 이번 구현에서 정한 비행 속도: 초당 200픽셀
FLY_SPEED_PPS = 200.0


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x = x
        self.y = y

        self.width = 100
        self.height = 100

        self.frame = 0.0

        # 1: 오른쪽, -1: 왼쪽
        self.direction = 1
        self.speed = FLY_SPEED_PPS

    def update(self):
        # 실제 경과 시간에 맞춰 날갯짓을 재생한다.
        self.frame = (
            self.frame
            + FRAMES_PER_SECOND * game_framework.frame_time
        ) % FRAME_COUNT

        # 이동 거리 = 방향 × 초당 속도 × 경과 시간
        self.x += (
            self.direction
            * self.speed
            * game_framework.frame_time
        )

        # 새의 이미지 전체가 화면 안에 있도록 경계를 설정한다.
        left_limit = self.width / 2
        right_limit = get_canvas_width() - self.width / 2

        # 경계를 넘어간 거리만큼 반대쪽으로 되돌려 반사한다.
        # 프레임 지연으로 여러 번 경계를 넘는 경우도 처리한다.
        while self.x < left_limit or self.x > right_limit:
            if self.x > right_limit:
                self.x = right_limit - (self.x - right_limit)
                self.direction = -1

            elif self.x < left_limit:
                self.x = left_limit + (left_limit - self.x)
                self.direction = 1

        # 경계에 정확히 도착한 경우에도 안쪽으로 방향을 바꾼다.
        if self.x == right_limit:
            self.direction = -1
        elif self.x == left_limit:
            self.direction = 1

    def draw(self):
        frame_index = int(self.frame)

        column = frame_index % FRAME_COLUMNS
        row = frame_index // FRAME_COLUMNS

        left = column * Bird.image.w // FRAME_COLUMNS
        right = (column + 1) * Bird.image.w // FRAME_COLUMNS

        top = row * Bird.image.h // FRAME_ROWS
        bottom = (row + 1) * Bird.image.h // FRAME_ROWS

        source_y = Bird.image.h - bottom

        # 원본은 오른쪽을 바라보므로 왼쪽 이동 시 수평 반전한다.
        flip = 'h' if self.direction == -1 else ''

        Bird.image.clip_composite_draw(
            left, source_y,
            right - left, bottom - top,
            0, flip,
            self.x, self.y,
            self.width, self.height
        )