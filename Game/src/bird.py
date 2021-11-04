from pyglet.graphics import Batch, OrderedGroup
from pyglet.sprite import Sprite
from src.data_loader import Assets, JsonData
from pyglet.image import Animation


class Bird(Sprite):
    """Bird
    -
    Class for a single Bird

    The bird class inherits from the pyglet.sprite.Sprite class.
    """

    def __init__(self, batch: Batch, group: OrderedGroup, assets: Assets, jData: JsonData) -> None:
        """__init__
        -
        Is called on class creation and setup a new bird.

        Args:
            batch (Batch): pyglet Batch in which the Bird is draw
            group (OrderedGroup): OrderedGroup to which the bird belongs (drawing level)
            assets (Assets): an instance of the Assets class (contains loaded sprite images)
            jData (JsonData): an instance of the JsonData class which contains game data like bird position
        """
        super().__init__(
            Animation.from_image_sequence(assets.birds, duration=0.1, loop=True),
            jData.birdPosX,
            ((jData.height + assets.base.height) - assets.birds[1].height) // 2,
            batch=batch,
            group=group,
        )
        self.assets = assets
        self.jData = jData

        # * :: Bird State ::
        self.alive = True
        self.velocity = 0

    def reset(self) -> None:
        """reset
        -
        Resets the birds values that may have changed during runtime and updates the sprite from the superclass.
        """
        self.alive = True
        self.velocity = 0
        self.image = Animation.from_image_sequence(self.assets.birds, duration=0.1, loop=True)
        super().update(
            y=((self.jData.height + self.assets.base.height) - self.assets.birds[1].height) // 2
        )

    def flap(self) -> None:
        """flap
        -
        Applys the force from the JsonData to the velocity of the bird
        """
        if self.alive:
            self.velocity = self.jData.birdFlapForce

    def checkForGround(self) -> bool:
        """checkForGround
        -
        Checks if the bird has touched the ground and if so keeps set prevents him from "falling" through the floor.

        Returns:
            bool: True -> the bird has hit the ground else -> False
        """
        if self.y <= self.assets.base.height:
            self.velocity = 0
            super().update(y=self.assets.base.height)
            return True
        return False

    def update(self, dt: float) -> bool:
        """update
        -
        Updates the birs velocity with the defined "gravity" from JasonData and the given "dt" value.\n
        Then the bird positon is change with the updated velocity.
        Afterwards the "checkForGround" function is applied

        Args:
            dt (float): time differents between the last update

        Returns:
            bool: True -> Bird is touching the ground else not
        """
        self.velocity -= self.jData.birdGravity * dt
        super().update(y=self.y + self.velocity * dt)
        self.checkForGround()
        return self.y <= self.assets.base.height
