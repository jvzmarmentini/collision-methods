import math
from typing import Tuple

from typing_extensions import Self


class Point:   
    def __init__(self, x:float=0, y:float=0, z:float=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"x={self.x:.3f}\ty={self.y:.3f}\tz={self.z:.3f}"

    def __add__(self, other:Self) -> Self:
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other:Self) -> Self:
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __mul__(self, other:float) -> Self:
        x = self.x * other
        y = self.y * other
        return Point(x, y)

    def set(self, x:float, y:float, z:float=0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def rotacionaZ(self, angulo:float) -> None:
        anguloRad = angulo * 3.14159265359/180.0
        xr = self.x*math.cos(anguloRad) - self.y*math.sin(anguloRad)
        yr = self.x*math.sin(anguloRad) + self.y*math.cos(anguloRad)
        self.x = xr
        self.y = yr

    def rotacionaY(self, angulo:float) -> None:
        anguloRad = angulo* 3.14159265359/180.0
        xr =  self.x*math.cos(anguloRad) + self.z*math.sin(anguloRad)
        zr = -self.x*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.x = xr
        self.z = zr
   
    def rotacionaX(self, angulo:float) -> None:
        anguloRad = angulo* 3.14159265359/180.0
        yr =  self.y*math.cos(anguloRad) - self.z*math.sin(anguloRad)
        zr =  self.y*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.y = yr
        self.z = zr

    @DeprecationWarning
    def intersec2d(k, l, m, n) -> Tuple[bool, float, float]:
        det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

        if (det == 0.0):
            return False, None, None # não há intersecção

        s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
        t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

        return True, s, t # há intersecção

    @DeprecationWarning
    def HaInterseccao(k, l, m, n) -> bool:
        ret, s, t = intersec2d( k,  l,  m,  n)

        if not ret: return False 

        return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0

