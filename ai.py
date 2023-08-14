import math
import random
import typing


def sigmoid(x):
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    else:
        z = math.exp(x)
        return z / (1 + z)


class LinNode:
    slope: float
    bias: float
    activation = sigmoid

    def __init__(self, slope=None, bias=None):
        self.slope = slope or random.random() - 0.5
        self.bias = bias or random.random() - 0.5

    def eval(self, x: float) -> float:
        return sigmoid(self.slope * x + self.bias)

    def mutated(self, mut_rate: float) -> "LinNode":
        mut_slope = self.slope + (random.random() - 0.5) * mut_rate
        mut_bias = self.bias + (random.random() - 0.5) * mut_rate
        return LinNode(mut_slope, mut_bias)

    def __repr__(self):
        return f"<Node: k:{self.slope:.2f} q:{self.bias:.2f}>"


class Layer:
    def __init__(self, nodes: list[LinNode], last=False):
        self.nodes = nodes
        self.last = last

    def eval(self, vec: typing.Iterable[float]) -> list[float] | float:
        if self.last:
            return sum(node.eval(x) for node, x in zip(self.nodes, vec)) / len(
                self.nodes
            )
        else:
            raise NotImplemented()

    def mutated(self, mut_rate: float) -> "Layer":
        mut_nodes = [node.mutated(mut_rate) for node in self.nodes]
        return Layer(mut_nodes, self.last)


class ModelSimple:
    def __init__(self, layer=None):
        self.layer = layer or Layer([LinNode(), LinNode()], True)

    def eval(self, vec: tuple[float, float]):
        return self.layer.eval(vec)

    def mutated(self, mut_rate: float) -> "ModelSimple":
        return self.__class__(self.layer.mutated(mut_rate))


class ModelSimplePred:
    def __init__(self, layer=None):
        self.layer = layer or Layer([LinNode(), LinNode(), LinNode()], True)

    def eval(self, vec: tuple[float, float, float]):
        return self.layer.eval(vec)
