from typing import Optional

import ai
import game


class AIBird:
    def __init__(self, bird, model=None):
        self.bird = bird
        self.model = model or ai.ModelSimple()

    def eval(self, state: game.GameState) -> None:
        next_pipe = self.get_next_pipe(state)
        if next_pipe is None:
            return

        x_diff = next_pipe.x - self.bird.x
        y_diff = next_pipe.y - self.bird.y
        ai_action = self.model.eval((x_diff, y_diff))
        if ai_action > 0.5:
            self.bird.jump()

    def get_next_pipe(self, state: game.GameState) -> Optional[game.Pipe]:
        for pipe in state.pipes:
            if pipe.x > self.bird.x:
                return pipe

    def mutated(self, bird: game.Bird, mut_rate: float) -> "AIBird":
        return AIBird(bird, self.model.mutated(mut_rate))
