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
    def drawAxis(Min: Point, Max: Point, Meio: Point) -> None:
        glLineWidth(1)
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        glVertex2f(Min.x, Meio.y)
        glVertex2f(Max.x, Meio.y)
        glVertex2f(Meio.x, Min.y)
        glVertex2f(Meio.x, Max.y)
        glEnd()
