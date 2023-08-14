import math
import random
import uuid

GRAVITY = 0.3
X_SPEED = 8
JUMP_DELAY = 30


class Bird:
    id: uuid.UUID
    x: float = 0
    y: float = 0
    y_vel: float = 0
    dead: bool = False
    jump_timer = 0

    def __init__(self, x=None, y=None):
        self.id = uuid.uuid4()
        self.x = x or 0
        self.y = y or 0

    def step(self):
        self.y_vel += GRAVITY
        self.y += self.y_vel
        self.x += X_SPEED
        self.jump_timer += 1

    def jump(self):
        if self.jump_timer > JUMP_DELAY:
            self.y_vel = -10
            self.jump_timer = 0

    def collides_with_pipe(self, pipe) -> bool:
        if abs(pipe.x - self.x) > 10:
            return False

        if abs(pipe.y - self.y) > (pipe.opening_size / 2 - 32):
            return True

        return False


class Pipe:
    id: uuid.UUID
    x: float
    y: float
    opening_size: float

    def __init__(self):
        self.id = uuid.uuid4()

    @classmethod
    def create_at(cls, x: float) -> "Pipe":
        pipe = Pipe()
        pipe.y = random.random() * 500
        pipe.opening_size = 200
        pipe.x = x
        return pipe


class GameState:
    pipes: list[Pipe]
    birds: list[Bird]
    counter = math.inf
    start_max_counter = 120
    max_counter = start_max_counter

    def __init__(self):
        self.pipes = []
        self.birds = []

    @property
    def score(self):
        return self.start_max_counter - self.max_counter

    def step(self):
        if self.counter > self.max_counter:
            self.pipes.append(Pipe.create_at(self.birds[0].x + 700))
            self.counter = 0
            self.max_counter -= 1
        else:
            self.counter += 1

        for bird in self.birds:
            bird.step()
            for pipe in self.pipes:
                if bird.collides_with_pipe(pipe):
                    bird.dead = True


class Game:
    def __init__(self):
        self.game_state = GameState()

    def step(self):
        self.game_state.step()
