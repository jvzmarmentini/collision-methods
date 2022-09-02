from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Polygon import *


class Drawer():
    @staticmethod
    def drawPolygon(polygon: Polygon, *color: float) -> None:
        if color is not None:
            glColor3f(*color)

        glLineWidth(3)
        glBegin(GL_LINE_LOOP)
        for vertices in polygon.Vertices:
            glVertex3f(vertices.x, vertices.y, vertices.z)
        glEnd()

    @staticmethod
    def drawPoints(polygon: Polygon, *color: float) -> None:
        if color is not None:
            glColor3f(*color)

        glPointSize(4)
        glBegin(GL_POINTS)
        for vertices in polygon.Vertices:
            glVertex3f(vertices.x, vertices.y, vertices.z)
        glEnd()

    @staticmethod
    def drawPoint(vertice: Point, *color: float) -> None:
        if color is not None:
            glColor3f(*color)
        glVertex3f(vertice.x, vertice.y, vertice.z)

    @staticmethod
    def drawBBox(polygon: Polygon, *color: float) -> None:
        assert len(polygon) == 2
        v = polygon.Vertices

        if color is not None:
            glColor3f(*color)

        glBegin(GL_LINE_LOOP)
        for o in [0, 1]:
            for i in [0, 1]:
                glVertex3f(v[o].x, v[(i + o) % 2].y, v[0].z)
        glEnd()

    @staticmethod
    def drawAxis(Min: Point, Max: Point, Meio: Point) -> None:
        glLineWidth(1)
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        glVertex2f(Min.x, Meio.y)
        glVertex2f(Max.x, Meio.y)
        glVertex2f(Meio.x, Min.y)
        glVertex2f(Meio.x, Max.y)
        glEnd()

    @staticmethod
    def drawListPoints(points: List[Point], *color: float) -> None:
        if color is not None:
            glColor3f(*color)

        for p in points:
            glVertex3f(p.x, p.y, p.z)

    @staticmethod
    def displayTitle(string, x, y):
        glColor3f( 1, 1, 1 )
        glRasterPos2f( x, y + 10 )
        for c in string:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))