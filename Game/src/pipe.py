from typing import List
from pyglet.graphics import Batch, OrderedGroup
from pyglet.sprite import Sprite
from src.ai.ai_bird import Ai_Bird
from src.bird import Bird
from src.data_loader import Assets, JsonData
from random import randint
from src.scoreBoard import ScoreBoard


class Pipe:
    """Pipe
    -
    Class for a Pipe -> includes the upper and lower pipe.
    """

    def __init__(
        self,
        x: float,
        assets: Assets,
        jData: JsonData,
        batch: Batch,
        group: OrderedGroup,
        mode: str = "normal",
        index: int = 0,
        bird: Bird = None,
        birds: List[Ai_Bird] = None,
    ) -> None:
        """__init__
        -
        Is called on class creation and setup a new pipe.

        Args:
            x (float): start value for the x positon of the pipe
            assets (Assets): an instance of the Assets class (contains loaded sprite images)
            jData (JsonData): an instance of the JsonData class which contains game data like the pipe gap size
            bird (Bird): the bird that is connected with the pipe
            index (int): 0 -> closest pipe to the bird the higher the index the further away the pipe from the bird
            batch (Batch): pyglet Batch in which the Pipe is draw
            group (OrderedGroup): OrderedGroup to which the pipe belongs (drawing level)
        """

        self.jData = jData
        self.assets = assets
        self.normal = mode == "normal"
        if self.normal:
            self.bird = bird
        else:
            self.birds: List[Ai_Bird] = birds

        # * :: Sprites ::
        self.lower = Sprite(img=assets.pipe, x=x, y=self.getY(), batch=batch, group=group)

        self.upper = Sprite(
            img=assets.pipe,
            x=x + assets.pipe.width,
            y=self.lower.y + assets.pipe.height * 2 + jData.pipeGapSizeY,
            batch=batch,
            group=group,
        )
        self.upper.rotation = 180

        self.positionID = index

    def getY(self) -> int:
        """getY
        -
        returns a random y Position inside the defined bounderies

        Returns:
            int: the random y Position
        """
        return randint(-self.jData.pipeLimitY, self.jData.pipeLimitY - self.jData.pipeGapSizeY)

    def update(self, other, dt: float, scoreBoard: ScoreBoard = None) -> None:
        """update
        -
        Updates the pipe and checks for collison with the bird.

        Args:
            other (Pipe): the other Pipe that is needed for a continuous loop
            scoreBoard (ScoreBoard): the ScoreBoard
            dt (float): time since the last call
        """
        if self.normal:
            if self.bird.alive:
                self.lower.update(x=self.lower.x - self.jData.baseScroll * dt)
                self.upper.update(x=self.upper.x - self.jData.baseScroll * dt)
                if self.positionID == 0:
                    self.check_for_collision()
                    if self.bird.x >= self.lower.x + self.assets.pipe.width:
                        scoreBoard.score += 1
                        scoreBoard.update()
                        self.positionID = 1
                        other.positionID = 0
                self.wrapAround(other)
        else:
            self.lower.update(x=self.lower.x - self.jData.baseScroll * dt)
            self.upper.update(x=self.upper.x - self.jData.baseScroll * dt)
            if self.positionID == 0:
                self.check_for_collision()
                for bird in self.birds:
                    if not bird.alive:
                        continue
                    updated = False
                    if bird.x >= self.lower.x + self.assets.pipe.width:
                        updated = True
                        bird.score += 1
                        bird.bonus = 0
                        bird.update(dt=dt)
                    if updated:
                        self.positionID = 1
                        other.positionID = 0
            self.wrapAround(other)

    def wrapAround(self, other, force: bool = False) -> None:
        """wrapAround
        -
        Moves the Pipe beind the other Pipe with the given distance from jData.

        Args:
            other (Pipe): the other Pipe that is needed for a continuous loop
            force (bool, optional): Forces the pipe to be wraped around even if not of screen jet. Defaults to False.
        """
        if self.lower.x + self.assets.pipe.width <= 0 or force:
            self.lower.update(x=other.lower.x + self.jData.pipeGapSizeX, y=self.getY())
            self.upper.update(
                x=other.upper.x + self.jData.pipeGapSizeX,
                y=self.lower.y + self.assets.pipe.height * 2 + self.jData.pipeGapSizeY,
            )

    def check_for_collision(self) -> None:
        """check_for_collision
        -
        Checks for collison of the bird and the pipe or the bird and the ground.
        """
        if self.normal:
            bottom_check: bool = self.bird.y >= self.lower.y + self.assets.pipe.height
            left_check: bool = self.bird.x + self.assets.birds[0].width >= self.lower.x
            right_check: bool = self.bird.x <= self.lower.x + self.assets.pipe.width
            top_check: bool = (
                self.bird.y + self.assets.birds[0].height
                <= self.lower.y + self.jData.pipeGapSizeY + self.assets.pipe.height
            )
            if (
                left_check and right_check and not (top_check and bottom_check)
            ) or self.bird.checkForGround():
                self.bird.alive = False
                self.bird.image = self.assets.birds[1]
        else:

            for bird in self.birds:
                bottom_check: bool = bird.y >= self.lower.y + self.assets.pipe.height
                left_check: bool = bird.x + self.assets.birds[0].width >= self.lower.x
                right_check: bool = bird.x <= self.lower.x + self.assets.pipe.width
                top_check: bool = (
                    bird.y + self.assets.birds[0].height
                    <= self.lower.y + self.jData.pipeGapSizeY + self.assets.pipe.height
                )
                if (
                    left_check and right_check and not (top_check and bottom_check)
                ) or bird.checkForGround():
                    bird.alive = False
                    bird.image = self.assets.birds[1]
