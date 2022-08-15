import abc
import random
import time

from ai_interface import AIBird
from drawer import PygameDrawer
from abc import ABC
from utils import Point

from game import Game, Bird
from termdraw import Screen


class BasePlayer(ABC):
    @abc.abstractmethod
    def play(self) -> None:
        ...


class HumanPlayer(BasePlayer):
    TIME_STEP = 1 / 30
    MAX_STEPS = int(2 / TIME_STEP)

    def play(self) -> None:
        game = Game()
        drawer = PygameDrawer()
        game.game_state.birds.append(bird := Bird())
        drawer.inp_callback = lambda x: bird.jump()
        while True:
            drawer.draw_state(game.game_state)
            game.step()


class AIPlayer(BasePlayer):
    GEN_SIZE = 200

    def __init__(self):
        self.game = Game()
        self.drawer = PygameDrawer()
        self.birds = [Bird(y=200) for _ in range(self.GEN_SIZE)]
        self.game.game_state.birds = self.birds
        self.ai_birds = {AIBird(bird) for bird in self.birds}

    def play(self) -> None:
        while True:
            last_ai_bird = None
            while self.ai_birds:
                self.drawer.draw_state(self.game.game_state)
                for ai_bird in self.ai_birds:
                    ai_bird.eval(self.game.game_state)

                self.game.step()
                to_remove = [ai_bird for ai_bird in self.ai_birds if ai_bird.bird.dead]
                for ai_bird in to_remove:
                    self.birds.remove(ai_bird.bird)
                    self.ai_birds.remove(ai_bird)
                    last_ai_bird = ai_bird

            self.birds = [Bird(y=200) for _ in range(self.GEN_SIZE)]
            self.game.game_state.birds = self.birds
            self.ai_birds = {last_ai_bird.mutated(bird, 0.05) for bird in self.birds}

            print(f"Best: {self.game.game_state.score}")

            # Add last best bird to the generation
            last_bird = Bird(y=200)
            self.birds.append(last_bird)
            self.ai_birds.add(AIBird(last_bird))
            self.game.game_state.pipes = []
            self.drawer.score = 0
            self.game.game_state.max_counter = self.game.game_state.start_max_counter
