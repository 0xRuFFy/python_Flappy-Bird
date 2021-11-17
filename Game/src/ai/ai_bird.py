from typing import List
from pyglet.graphics import Batch, OrderedGroup
from src.data_loader import Assets, JsonData
from src.bird import Bird
from src.ai.ann import Ann


class Ai_Bird(Bird):
    def __init__(self, batch: Batch, group: OrderedGroup, assets: Assets, jData: JsonData) -> None:
        super().__init__(batch, group, assets, jData)

        self.ann: Ann = Ann(jData.ann_struct)
        self.fitnes: int
        self.score: int = 0
        self.bonus: float = 0.0

    def _reset(self, anc: List[List[float]], copy: bool = False):
        self.reset()
        self.ann.connections = self.ann.create_connections(ancestor=anc, copy=copy)
    
    def _update(self, dt: float = 0) -> None:
        if self.ann.compute_output() == 0:
            self.flap()
            
        self.update(dt=dt)
        self.bonus += dt
        
    def set_input_layer(self, in_layer: List[float]) -> None:
        self.ann.set_input_layer(in_layer)

    def get_fitnes(self) -> None:
        self.visible = False
        self.fitnes = self.score + self.bonus

    def get_gens(self) -> List[List[float]]:
        return [[i for i in n] for n in self.ann.connections]
