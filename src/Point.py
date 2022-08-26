import math
from typing import Tuple
from typing_extensions import Self

class Point:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"x={self.x:.3f}\ty={self.y:.3f}\tz={self.z:.3f}"

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __mul__(self, other: int):
        x = self.x * other
        y = self.y * other
        return Point(x, y)

    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def rotacionaZ(self, angulo) -> Self:
        anguloRad = angulo * 3.14159265359/180.0
        xr = self.x*math.cos(anguloRad) - self.y*math.sin(anguloRad)
        yr = self.x*math.sin(anguloRad) + self.y*math.cos(anguloRad)
        self.x = xr
        self.y = yr

        return self

    def rotacionaY(self, angulo):
        anguloRad = angulo* 3.14159265359/180.0
        xr =  self.x*math.cos(anguloRad) + self.z*math.sin(anguloRad)
        zr = -self.x*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.x = xr
        self.z = zr
   
    def rotacionaX(self, angulo):
        anguloRad = angulo* 3.14159265359/180.0
        yr =  self.y*math.cos(anguloRad) - self.z*math.sin(anguloRad)
        zr =  self.y*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.y = yr
        self.z = zr

    def intersec2d(k, l, m, n) -> Tuple[bool, float, float]:
        det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

        if (det == 0.0):
            return False, None, None # não há intersecção

        s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
        t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

        return True, s, t # há intersecção

    def HaInterseccao(k, l, m, n) -> bool:
        ret, s, t = intersec2d( k,  l,  m,  n)

        if not ret: return False 

        return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0

