from pyglet.image import load, AbstractImage
from typing import Dict, List
import json


class JsonData:
    """JsonData
    -
    Loads all values from the json data file.
    """

    with open("./data/data.json") as file:
        data: Dict = json.load(file)

        width: int = data["window"]["width"]
        height: int = data["window"]["height"]
        baseScroll: int = data["game"]["basescroll"]
        fps_dt: float = 1 / data["window"]["fps"]
        birdPosX: int = data["bird"]["xpos"]
        birdFlapForce: float = data["bird"]["flapforce"]
        birdGravity: int = data["bird"]["gravity"]
        pipeLimitY: int = data["pipe"]["limit"]
        pipeGapSizeY: int = data["pipe"]["gapY"]
        pipeGapSizeX: int = data["pipe"]["gapX"]
        scoreBoardX: int = data["scoreboard"]["x"]
        scoreBoardY: int = data["scoreboard"]["y"]


class Assets:
    """Assets
    -
    Loads all images into memory.
    """

    path: str = "./data/assets"

    def __init__(self) -> None:
        self.birds: List[AbstractImage] = [
            load(f"{self.path}/bird/bird_midflap.png"),
            load(f"{self.path}/bird/bird_downflap.png"),
            load(f"{self.path}/bird/bird_upflap.png"),
        ]
        self.numbers: List[AbstractImage] = [
            load(f"{self.path}/numbers/{i}.png") for i in range(10)
        ]
        self.pipe: AbstractImage = load(f"{self.path}/pipe.png")
        self.background: AbstractImage = load(f"{self.path}/background.png")
        self.base: AbstractImage = load(f"{self.path}/base.png")
        self.icon: AbstractImage = load(f"{self.path}/favicon.ico")
        self.startScreen: AbstractImage = load(f"{self.path}/message.png")
        self.gameOver: AbstractImage = load(f"{self.path}/gameover.png")
