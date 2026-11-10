from pico2d import load_image, get_canvas_width

import game_framework


FRAME_COLUMNS = 5
FRAME_ROWS = 3
FRAME_COUNT = 14

# 1초에 14프레임: 날갯짓 한 사이클
FRAMES_PER_SECOND = 14.0

# 초당 이동 거리
FLY_SPEED_PPS = 200.0


class Bird:
    image = None

    def __init__(self, x=800, y=400, direction=1, frame=0.0):
        # 모든 새가 이미지 한 장을 공유한다.
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        # 위치, 방향, 현재 프레임은 새마다 따로 관리한다.
        self.x = x
        self.y = y

        self.width = 100
        self.height = 100

        self.frame = float(frame) % FRAME_COUNT
        self.direction = direction
        self.speed = FLY_SPEED_PPS

    def update(self):
        # 경과 시간에 맞춰 날갯짓 프레임을 증가시킨다.
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

        # 이미지 전체가 화면 안에 들어오도록 경계를 설정한다.
        left_limit = self.width / 2
        right_limit = get_canvas_width() - self.width / 2

        # 경계를 초과한 거리를 반대 방향으로 반사한다.
        while self.x < left_limit or self.x > right_limit:
            if self.x > right_limit:
                self.x = right_limit - (self.x - right_limit)
                self.direction = -1

            elif self.x < left_limit:
                self.x = left_limit + (left_limit - self.x)
                self.direction = 1

        # 경계에 정확히 도착한 경우에도 방향을 전환한다.
        if self.x == right_limit:
            self.direction = -1
        elif self.x == left_limit:
            self.direction = 1

    def draw(self):
        # 소수 프레임은 유지하고, 그릴 때만 정수로 변환한다.
        frame_index = int(self.frame)

        # 위쪽 줄부터 왼쪽 → 오른쪽 순서로 읽는다.
        column = frame_index % FRAME_COLUMNS
        row = frame_index // FRAME_COLUMNS

        # 이미지 크기가 칸 수로 나누어떨어지지 않으므로
        # 각 칸의 시작과 끝을 따로 계산한다.
        left = column * Bird.image.w // FRAME_COLUMNS
        right = (column + 1) * Bird.image.w // FRAME_COLUMNS

        top = row * Bird.image.h // FRAME_ROWS
        bottom = (row + 1) * Bird.image.h // FRAME_ROWS

        # pico2d는 이미지 아래쪽을 기준으로 좌표를 계산한다.
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