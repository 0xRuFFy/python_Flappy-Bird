from typing import List
from pyglet.graphics import Batch, OrderedGroup
from pyglet.sprite import Sprite
from src.data_loader import Assets, JsonData


class ScoreBoard:
    """ScoreBoard
    -
    Class to display the current score using the number images
    """

    def __init__(self, assets: Assets, jData: JsonData, batch: Batch, group: OrderedGroup) -> None:
        self.jData = jData
        self.assets = assets
        self.batch = batch
        self.group = group

        self.score = 0
        self.scoreSprites: List[Sprite] = [
            Sprite(
                img=assets.numbers[0],
                x=jData.scoreBoardX,
                y=jData.scoreBoardY,
                batch=batch,
                group=group,
            )
        ]

    def visibility(self, opacity: int) -> None:
        for sprite in self.scoreSprites:
            sprite.opacity = opacity

    def update(self) -> None:
        imgNeeded = [int(d) for d in str(self.score)]
        x = self.jData.scoreBoardX - (self.assets.numbers[0].width / 2 + 2) * (len(imgNeeded) // 2)
        self.scoreSprites = []
        for i in imgNeeded:
            self.scoreSprites.append(
                Sprite(
                    img=self.assets.numbers[i],
                    x=x,
                    y=self.jData.scoreBoardY,
                    batch=self.batch,
                    group=self.group,
                )
            )
            x += self.assets.numbers[i].width
