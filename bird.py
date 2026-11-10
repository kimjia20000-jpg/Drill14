from pico2d import load_image


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        # 모든 새가 같은 이미지를 공유한다.
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x = x
        self.y = y

        self.width = 100
        self.height = 100

    def update(self):
        pass

    def draw(self):
        # 스프라이트 시트: 가로 5칸, 세로 3줄
        # 첫 프레임은 맨 위 왼쪽에 있다.
        cell_width = Bird.image.w // 5
        cell_height = Bird.image.h // 3

        # pico2d의 이미지 자르기 좌표는 아래쪽이 기준이다.
        source_y = Bird.image.h - cell_height

        Bird.image.clip_draw(
            0, source_y,
            cell_width, cell_height,
            self.x, self.y,
            self.width, self.height
        )