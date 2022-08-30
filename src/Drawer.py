from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Polygon import *


class Drawer():
    @staticmethod
    def drawPolygon(polygon: Polygon, *color: float) -> None:
        if color is not None:
            glColor3f(*color)
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
        glBegin(GL_POINTS)
        glVertex3f(vertice.x, vertice.y, vertice.z)
        glEnd()

    @staticmethod
    def drawBBox(vertices: list, *color: float) -> None:
        if color is not None:
            glColor3f(*color)

        glBegin(GL_LINE_LOOP)
        glVertex3f(vertices[0].x, vertices[0].y, vertices[0].z)
        glVertex3f(vertices[1].x, vertices[0].y, vertices[0].z)
        glVertex3f(vertices[1].x, vertices[1].y, vertices[0].z)
        glVertex3f(vertices[0].x, vertices[1].y, vertices[0].z)
        glEnd()

    @staticmethod
    def drawAxis(amin: Point, amax: Point, mid: Point) -> None:
        glColor3f(0, 0, 0)

        glBegin(GL_LINES)
        glVertex2f(amin.x, mid.y)
        glVertex2f(amax.x, mid.y)
        glVertex2f(mid.x, amin.y)
        glVertex2f(mid.x, amax.y)
        glEnd()
