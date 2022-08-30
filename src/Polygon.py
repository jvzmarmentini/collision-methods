import copy

from multipledispatch import dispatch
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Point import *


class Polygon:
    def __init__(self):
        self.Vertices = []

    def __len__(self):
        return len(self.Vertices)

    def __str__(self) -> str:
        return '\n'.join([str(x) for x in self.Vertices])

    @dispatch(float, float, float)
    def insertVertice(self, x: float, y: float, z: float = 0.0) -> None:
        self.Vertices.append(Point(x, y, z))

    @dispatch(Point)
    def insertVertice(self, p: Point) -> None:
        self.Vertices.append(p)

    def getVertice(self, i) -> Point:
        return copy.deepcopy(self.Vertices[i])

    def getLimits(self) -> Tuple[Point]:
        assert len(self.Vertices) > 0

        Min = copy.deepcopy(self.Vertices[0])
        Max = copy.deepcopy(self.Vertices[0])

        Min.x = min([v.x for v in self.Vertices])
        Min.y = min([v.y for v in self.Vertices])
        Min.z = min([v.z for v in self.Vertices])

        Max.x = max([v.x for v in self.Vertices])
        Max.y = max([v.y for v in self.Vertices])
        Max.z = max([v.z for v in self.Vertices])

        return Min, Max

    def modifyVertice(self, i, P):
        self.Vertices[i] = P

    def getEdge(self, n: int) -> Point:
        v1 = self.Vertices[n]
        v2 = self.Vertices[(n+1) % len(self)]
        return v2 - v1

    def isPointInside(self, p: Point) -> bool:
        prod = []

        for i, v in enumerate(self.Vertices):
            polyEdge = self.getEdge(i)
            pointEdge = p - v
            prod.append(polyEdge.x * pointEdge.y - polyEdge.y * pointEdge.x)

        return all(n < 0 for n in prod) or all(n >= 0 for n in prod)
