from typing import List, Tuple
from pyglet.graphics import Batch, OrderedGroup
from pyglet.text import Label
from src.data_loader import Assets, JsonData
from src.scoreBoard import ScoreBoard
from src.ai.ai_bird import Ai_Bird
from src.pipe import Pipe


class infoText(Label):
    def __init__(self, text, value=0, x=0, y=0, batch=None, group=None):
        super().__init__(
            text=f"{text}: {value}",
            font_name="Arial",
            font_size=15,
            color=(255, 255, 255, 255),
            x=x,
            y=y,
            anchor_x="left",
            anchor_y="baseline",
            batch=batch,
            group=group,
        )
        self.info = text

    def updateValue(self, value) -> None:
        self.text = f"{self.info}: {value}"


class Generation:
    def __init__(
        self,
        size: int,
        bird_setup: Tuple,
        pipe_setup: Tuple,
        batch: Batch,
        uigroup: OrderedGroup,
        jData: JsonData,
        assets: Assets,
    ) -> None:

        self.birds: List[Ai_Bird] = [Ai_Bird(*bird_setup) for _ in range(size)]
        self.pipes: List[Pipe] = [
            Pipe(*(pipe_setup), index=0, birds=self.birds, mode="learn"),
            Pipe(*(pipe_setup), index=1, birds=self.birds, mode="learn"),
        ]
        self.pipes[1].wrapAround(self.pipes[0], force=True)
        self.pipe_setup = pipe_setup

        self.gen = 1
        self.maxScore = 0
        self.scoreBoard = ScoreBoard(assets, jData, batch, uigroup)
        self.info: List[infoText] = [
            infoText("Gen", value=self.gen, x=10, y=60, batch=batch, group=uigroup),
            infoText("maxScore", value=self.maxScore, x=10, y=40, batch=batch, group=uigroup),
        ]

    def update(self, dt: float = 0) -> None:
        self.set_birds_input_layer()
        d_count = 0
        for bird in self.birds:
            if bird.alive:
                bird._update(dt=dt)
                if bird.score >= self.scoreBoard.score:
                    self.scoreBoard.score = bird.score
                    self.scoreBoard.update()
            else:
                d_count += 1
                bird.get_fitnes(pipe=self.get_next_pipe())

        if d_count == len(self.birds):
            self.gen += 1
            self.info[0].updateValue(self.gen)
            self.create_next_gen()

            del self.pipes
            self.pipes: List[Pipe] = [
                Pipe(*(self.pipe_setup), index=0, birds=self.birds, mode="learn"),
                Pipe(*(self.pipe_setup), index=1, birds=self.birds, mode="learn"),
            ]
            self.pipes[1].wrapAround(self.pipes[0], force=True)

        self.pipes[0].update(self.pipes[1], dt=dt)
        self.pipes[1].update(self.pipes[0], dt=dt)

    def set_birds_input_layer(self) -> None:
        next_pipe: Pipe = self.get_next_pipe()

        for bird in self.birds:
            if bird.alive:
                top = next_pipe.upper.y - bird.y - bird.height
                right = next_pipe.lower.x - bird.x - bird.width
                bot = bird.y - next_pipe.lower.y - next_pipe.lower.height
                left = bird.x - next_pipe.lower.x - next_pipe.lower.width
                bird.set_input_layer([top, bot, right, left])

    def get_next_ancestor(self) -> List[float]:
        best = -1
        best_id: int
        for i, bird in enumerate(self.birds):
            if bird.fitnes > best:
                best = bird.fitnes
                best_id = i

        if best == -1:
            raise IndexError("No Bird has a fitnes")

        return self.birds[best_id].get_gens()

    def create_next_gen(self) -> None:
        if self.scoreBoard.score > self.maxScore:
            self.maxScore = self.scoreBoard.score
            self.info[1].updateValue(self.maxScore)
        self.scoreBoard.score = 0
        self.scoreBoard.update()
        
        anc = self.get_next_ancestor()
        self.birds[0]._reset(anc, copy=True)
        for bird in self.birds[1:]:
            bird._reset(anc)

    def get_next_pipe(self) -> Pipe:
        return self.pipes[0] if self.pipes[0].positionID == 0 else self.pipes[1]
