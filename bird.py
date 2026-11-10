from pico2d import load_image

import game_framework


# 이미지 배열: 가로 5칸, 세로 3줄
FRAME_COLUMNS = 5
FRAME_ROWS = 3

# 마지막 줄의 빈칸을 제외한 실제 프레임 수
FRAME_COUNT = 14

# 날갯짓 한 사이클을 1초에 재생하도록 설정
FRAMES_PER_SECOND = 14.0


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        # 새들이 같은 이미지 리소스를 공유한다.
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x = x
        self.y = y

        self.width = 100
        self.height = 100

        # 소수 부분까지 누적하여 시간에 맞게 재생한다.
        self.frame = 0.0

    def update(self):
        self.frame = (
            self.frame
            + FRAMES_PER_SECOND * game_framework.frame_time
        ) % FRAME_COUNT

    def draw(self):
        # 그릴 때만 정수 프레임 번호로 변환한다.
        frame_index = int(self.frame)

        # 위쪽 줄부터 왼쪽 → 오른쪽 순서로 읽는다.
        column = frame_index % FRAME_COLUMNS
        row = frame_index // FRAME_COLUMNS

        # 이미지 크기가 칸 수로 나누어떨어지지 않으므로
        # 각 칸의 시작과 끝 좌표를 따로 계산한다.
        left = column * Bird.image.w // FRAME_COLUMNS
        right = (column + 1) * Bird.image.w // FRAME_COLUMNS

        top = row * Bird.image.h // FRAME_ROWS
        bottom = (row + 1) * Bird.image.h // FRAME_ROWS

        # 위에서 센 좌표를 pico2d의 아래쪽 기준 좌표로 변환한다.
        source_y = Bird.image.h - bottom

        Bird.image.clip_draw(
            left, source_y,
            right - left, bottom - top,
            self.x, self.y,
            self.width, self.height
        )