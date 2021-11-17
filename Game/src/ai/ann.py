from typing import List
from random import uniform, random
from math import exp


class Ann:

    m_rate = 0.05

    def __init__(self, struct: List[int]) -> None:
        self.layers: List[List[float]] = [[0 for _ in range(i)] for i in struct]
        self.connections: List[List[float]] = self.create_connections(init=True)

    def create_connections(
        self, init: bool = False, ancestor: List[float] = None, copy: bool = False
    ) -> List[List[float]]:
        if init:
            return [
                [self.get_rand_weight() for _ in range(len(self.layers[i]) * len(layer))]
                for i, layer in enumerate(self.layers[1:])
            ]
        elif ancestor != None:
            return [
                [
                    self.get_rand_weight(else_value=ancestor[i][j]) if not copy else ancestor[i][j]
                    for j in range(len(self.layers[i]) * len(layer))
                ]
                for i, layer in enumerate(self.layers[1:])
            ]
        else:
            raise ValueError

    def compute_output(self) -> int:
        #  go through all the layer with offset 1
        for x in range(1, len(self.layers)):
            #  go through all nodes of current layer
            for i in range(len(self.layers[x])):
                #  reset current nodes value
                self.layers[x][i] = 0
                #  go through all nodes of the previous layer
                for j in range(len(self.layers[x - 1])):
                    #  add wighted node value to current node
                    self.layers[x][i] += (
                        self.layers[x - 1][j]
                        * self.connections[x - 1][j + i * len(self.layers[x - 1])]
                    )
                #  apply sigma funktion if not the output layer
                if x != len(self.layers) - 1:
                    self.layers[x][i] = self.sigma(self.layers[x][i])

        return self.layers[-1].index(max(self.layers[-1]))

    def set_input_layer(self, in_layer: List[float]) -> None:
        for i, node in enumerate(in_layer):
            self.layers[0][i] = node / 1000
    
    def get_rand_weight(self, else_value: float = 0) -> float:
        if random() <= self.m_rate:
            return uniform(-1, 1)
        return else_value

    @staticmethod
    def sigma(x: float) -> float:
        return 1 / (1 + exp(-x))


if __name__ == "__main__":

    ann = Ann([4, 3, 2])
    print(ann.layers)
    print(ann.connections)

    print(ann.compute_output())
    print(ann.layers)
