from typing import Literal
from pyglet.window import Window, key, mouse
from src.bird import Bird
from src.pipe import Pipe
from src.data_loader import Assets, JsonData
from pyglet.graphics import Batch, OrderedGroup
from pyglet.clock import schedule_interval
from pyglet.sprite import Sprite
from src.scoreBoard import ScoreBoard
from pyglet.shapes import Rectangle

from src.ai.generation import Generation


class FlappyWindow(Window):
    """FlappyWindow
    -
    Class for a Game window for FlappyBird\n
    Handels the Gameloop aswell as Gameobject creation and Keyboard inputs
    """

    # * :: data Classes ::
    jData = JsonData()
    assets = Assets()

    def __init__(self, mode: str = "play", gen_size: int = None) -> None:
        """Creates a Flappy Bird Window"""
        # * :: Window Setup ::
        super(FlappyWindow, self).__init__(
            self.jData.width, self.jData.height, caption="Flappy Bird", style="dialog", vsync=True
        )
        self.set_icon(self.assets.icon)

        # * :: Windowstate Vars ::
        self.run_ml = mode == "learn"
        self.running = False
        self.restartable = False

        # * :: Graphics utility ::
        self.gameBatch = Batch()
        self.groups = [OrderedGroup(i) for i in range(6)]

        # * :: Sprites ::
        self.bgSprite = Sprite(
            self.assets.background, 0, 0, batch=self.gameBatch, group=self.groups[0]
        )

        if not self.run_ml:
            self.startMessage = Sprite(
                self.assets.startScreen, x=0, y=0, group=self.groups[5], batch=self.gameBatch
            )
            self.startMessage.position = (
                (self.width - self.startMessage.width) // 2,
                (self.height - self.startMessage.height) // 2,
            )

            self.gameOver_message = Sprite(
                self.assets.gameOver, 0, 0, group=self.groups[5], batch=self.gameBatch
            )
            self.gameOver_message.position = (
                (self.width - self.gameOver_message.width) // 2,
                self.height // 3 * 2,
            )
            self.gameOver_message.opacity = 0

            self.grey_screen = Rectangle(
                0,
                0,
                self.width,
                self.height,
                color=(0, 0, 0),
                batch=self.gameBatch,
                group=self.groups[4],
            )
            self.grey_screen.opacity = 0

            self.bird = Bird(self.gameBatch, self.groups[2], self.assets, self.jData)

            self.pipes = [
                Pipe(
                    self.width,
                    self.assets,
                    self.jData,
                    self.gameBatch,
                    self.groups[1],
                    index=0,
                    bird=self.bird,
                ),
                Pipe(
                    self.width + self.jData.pipeGapSizeX,
                    self.assets,
                    self.jData,
                    self.gameBatch,
                    self.groups[1],
                    index=1,
                    bird=self.bird,
                ),
            ]
        else:
            self.gen = Generation(
                gen_size,
                (self.gameBatch, self.groups[2], self.assets, self.jData),
                (self.width, self.assets, self.jData, self.gameBatch, self.groups[1]),
                self.gameBatch,
                self.groups[-1],
                self.jData,
                self.assets
            )

        self.bases = [
            Sprite(
                self.assets.base,
                self.assets.base.width * i,
                0,
                batch=self.gameBatch,
                group=self.groups[3],
            )
            for i in range(2)
        ]

        self.scoreBoard = ScoreBoard(self.assets, self.jData, self.gameBatch, self.groups[4])
        self.scoreBoard.visibility(0)

        # * :: schedule_interval for .update ::
        schedule_interval(self.update, self.jData.fps_dt)

    def newGame(self):
        self.gameOver_message.opacity = 0
        self.grey_screen.opacity = 0
        self.scoreBoard.score = 0
        self.scoreBoard.update()

        del self.pipes
        self.pipes = [
            Pipe(
                self.width,
                self.assets,
                self.jData,
                self.gameBatch,
                self.groups[1],
                index=0,
                bird=self.bird,
            ),
            Pipe(
                self.width + self.jData.pipeGapSizeX,
                self.assets,
                self.jData,
                self.gameBatch,
                self.groups[1],
                index=1,
                bird=self.bird,
            ),
        ]
        self.bird.reset()

    def baseScroll(self, dt) -> None:
        """Function to move and wrap around the to Base Sprits in .bases[]

        Args:
            dt (float): time delta for smooth gameupdates -> handelt by schedule_interval()
        """
        if self.run_ml or self.bird.alive:
            self.bases[0].x = self.bases[0].x - self.jData.baseScroll * dt
            self.bases[1].x -= self.jData.baseScroll * dt

            if self.bases[0].x + self.assets.base.width <= 0:
                self.bases[0].x = self.bases[1].x + self.assets.base.width

            if self.bases[1].x + self.assets.base.width <= 0:
                self.bases[1].x = self.bases[0].x + self.assets.base.width

    def update(self, dt=0.0):
        """Update all moving Parts in the Screen

        Args:
            dt (float): time delta for smooth gameupdates -> handelt by schedule_interval(). Defaults to 0.
        """
        self.baseScroll(dt=dt)

        if self.run_ml:
            # - TODO: implement update function for ai
            self.gen.update(dt=dt)
        elif self.running:
            self.restartable = self.bird.update(dt=dt)

            if not self.bird.alive:
                self.gameOver_message.opacity = 255
                self.grey_screen.opacity = 100
                self.scoreBoard.visibility(0)

            self.pipes[0].update(self.pipes[1], scoreBoard=self.scoreBoard, dt=dt)
            self.pipes[1].update(self.pipes[0], scoreBoard=self.scoreBoard, dt=dt)

    def on_draw(self) -> None:
        """Clear the Window and redraw the batch"""
        self.clear()
        self.gameBatch.draw()

    def on_key_press(self, symbol: Literal[32], modifiers):
        """Function to handel keypresses

        Args:
            symbol (Literal[32]): Pressed Key in Literal[32]
        """
        if not self.run_ml:
            if symbol == key.SPACE:
                self.bird.flap()
                if not self.running:
                    self.running = True
                    self.startMessage.opacity = 0
                    self.scoreBoard.visibility(255)

            if not self.bird.alive and self.restartable and symbol == key.SPACE:
                self.newGame()

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.run_ml:
            if button == mouse.LEFT:
                self.bird.flap()
                if not self.running:
                    self.running = True
                    self.startMessage.opacity = 0
                    self.scoreBoard.visibility(255)

            if not self.bird.alive and self.restartable and button == mouse.LEFT:
                self.newGame()
