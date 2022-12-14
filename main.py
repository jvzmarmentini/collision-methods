# -*- coding: utf-8 -*-
import argparse
import copy
import os
import random
import string
import time
from functools import reduce
from turtle import pos
from typing import List

from anytree import Node, PreOrderIter, RenderTree
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Drawer import *
from src.Point import *
from src.Polygon import *

PontosDoCenario = Polygon()
CampoDeVisao = Polygon()
TrianguloBase = Polygon()
PosicaoDoCampoDeVisao = Point()
BBox = Polygon()

AnguloDoCampoDeVisao = 0.0

Min = Point()
Max = Point()
Meio = Point()
Tamanho = Point()
TamanhoCampoVisao = .25

PontoClicado = Point()

flagDesenhaEixos = True

QTRoot = None
# QTColor = [[random.random() for _ in range(3)] for _ in range(20)]
QTColor = [[0,.9,.5],[.8,0,1],[1,.6,.2],[0,.9,.5],[.8,0,1],[1,.6,.2],[0,.9,.5],[.8,0,1],[1,.6,.2]]
QTMinN = 10
QTBBoxPrecision = 5
QTShowAll = True

performance = {}
overhead = {"initQuadTree total overhead": 0}
total = 0
pos = None


def raw():
    global total

    glPointSize(4)
    glBegin(GL_POINTS)

    for p in PontosDoCenario.Vertices:
        total += 1
        Drawer.drawPoint(p, 1, 0, 0)

    glEnd()


def bruteForce():
    performance.update({"bruteForce": 0})

    glPointSize(4)
    glBegin(GL_POINTS)

    for p in PontosDoCenario.Vertices:
        performance["bruteForce"] += 1
        if CampoDeVisao.isPointInside(p):
            Drawer.drawPoint(p, 0, 1, 0)
        else:
            Drawer.drawPoint(p, 1, 0, 0)

    glEnd()


def envelope():
    performance.update({"bruteForce": 0, "envelope x point": 0})
    Drawer.drawBBox(BBox, 3, 0, 1, 1)

    glPointSize(4)
    glBegin(GL_POINTS)
    for p in PontosDoCenario.Vertices:
        performance["envelope x point"] += 1
        if BBox.isPointInsideBox(p):
            Drawer.drawPoint(p, 1, 0, 0)
        else:
            performance["bruteForce"] += 1
            if CampoDeVisao.isPointInside(p):
                Drawer.drawPoint(p, 0, 1, 0)
            else:
                Drawer.drawPoint(p, 1, 1, 0)

    glEnd()


def initQuadTree() -> Node:
    start = time.time()

    quadTreePoints = copy.deepcopy(PontosDoCenario.Vertices)
    quadTreeRoot = Node("q", poly=Polygon(Min, Max), inside=[])
    _initQuadTree(Min, Max, quadTreeRoot, quadTreePoints)

    end = time.time() - start

    overhead["initQuadTree total overhead"] += end
    overhead["initQuadTree overhead"] = end

    return quadTreeRoot


def _initQuadTree(gmin: Point, gmax: Point, parent: Node, points: List[Point]) -> None:
    alp = ['a', 'b', 'c', 'd']

    mid = (gmin + gmax) * .5
    delta = mid - gmin
    prc = 10 ** -QTBBoxPrecision

    for s in [0, 1]:
        for c in [0, 1]:
            name = parent.name + alp.pop(0)
            lmin = Point(gmin.x + c * (delta.x + prc),
                         gmin.y + s * (delta.y + prc))
            lmax = Point(mid.x + c * delta.x,
                         mid.y + s * delta.y)
            poly = Polygon(lmin, lmax)

            inside = list(
                filter(lambda p: not poly.isPointInsideBox(p), points))

            node = Node(name=name, poly=poly, parent=parent, inside=inside)
            if len(inside) > QTMinN:
                _initQuadTree(lmin, lmax, node, inside)


def quadTree():
    global Min, Max, BBoxm, QTRoot, QTColor
    
    performance.update({"bruteForce": 0, "envelope x envelope": 0}) 
    Drawer.drawBBox(BBox, 3, 0, 1, 1)

    for leafNode in PreOrderIter(QTRoot, filter_=lambda n: n.is_leaf):
        performance["envelope x envelope"] += 1
        if not BBox.collisionWithBBox(leafNode.poly):
            if QTShowAll:
                Drawer.drawBBox(leafNode.poly, 1, *QTColor[leafNode.depth])

            glPointSize(4)
            glBegin(GL_POINTS)
            for p in leafNode.inside:
                Drawer.drawPoint(p, 1, 0, 0)
            glEnd()
        else:
            Drawer.drawBBox(leafNode.poly, 1, *QTColor[leafNode.depth])

            glPointSize(4)
            glBegin(GL_POINTS)
            for p in leafNode.inside:
                performance["bruteForce"] += 1
                if CampoDeVisao.isPointInside(p):
                    Drawer.drawPoint(p, 0, 1, 0)
                else:
                    Drawer.drawPoint(p, 1, 1, 0)
            glEnd()


queue = [bruteForce, envelope, quadTree]

def generatePoints(qtd, Min: Point, Max: Point) -> Polygon:
    Escala = (Max - Min) * (1.0/1000.0)

    for _ in range(qtd):
        x = random.randint(0, 1000) * Escala.x + Min.x
        y = random.randint(0, 1000) * Escala.y + Min.y
        PontosDoCenario.insertVertice(x, y)

    return PontosDoCenario


def readFromFile(filepath: str) -> Polygon:
    with open(filepath) as f:
        for line in f:
            words = line.split()
            x = float(words[0])
            y = float(words[1])
            PontosDoCenario.insertVertice(x, y)

    return PontosDoCenario


def CriaTrianguloDoCampoDeVisao():
    global TrianguloBase, CampoDeVisao

    vetor = Point(1.0, 0.0)
    TrianguloBase.insertVertice(0.0, 0.0)
    CampoDeVisao.insertVertice(0.0, 0.0)

    vetor.rotateZ(45)
    TrianguloBase.insertVertice(vetor.x, vetor.y)
    CampoDeVisao.insertVertice(vetor.x, vetor.y)

    vetor.rotateZ(-90)
    TrianguloBase.insertVertice(vetor.x, vetor.y)
    CampoDeVisao.insertVertice(vetor.x, vetor.y)


def PosicionaTrianguloDoCampoDeVisao():
    tam = Tamanho.x * TamanhoCampoVisao
    for i in range(len(TrianguloBase)):
        temp = TrianguloBase.getVertice(i).rotateZ(AnguloDoCampoDeVisao)
        CampoDeVisao.modifyVertice(i, PosicaoDoCampoDeVisao + temp*tam)

    min, max = CampoDeVisao.getLimits()
    BBox.modifyVertice(0, min)
    BBox.modifyVertice(1, max)


def AvancaCampoDeVisao(distancia):
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao
    vetor = Point(1, 0, 0)
    vetor.rotateZ(AnguloDoCampoDeVisao)
    PosicaoDoCampoDeVisao = PosicaoDoCampoDeVisao + vetor * distancia


def init(filepath: string) -> None:
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao
    global Min, Max, Meio, Tamanho
    global QTRoot

    glClearColor(0, 0, 0, 1)

    if filepath is None:
        Min, Max = generatePoints(1000, Point(
            0, 0), Point(500, 500)).getLimits()
    else:
        Min, Max = readFromFile(filepath).getLimits()

    Meio = (Max+Min) * 0.5  # Point central da janela
    Tamanho = (Max - Min)  # Tamanho da janela em X,Y

    PosicaoDoCampoDeVisao = Meio
    AnguloDoCampoDeVisao = 0

    # Cria o triangulo que representa o campo de visao
    CriaTrianguloDoCampoDeVisao()

    min, max = CampoDeVisao.getLimits()
    BBox.insertVertice(min)
    BBox.insertVertice(max)

    PosicionaTrianguloDoCampoDeVisao()
    QTRoot = initQuadTree()
    
    PosicionaCampoDeVisao(1)


def reshape(w, h):
    global Min, Max

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selec??o, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    # os.system('cls' if os.name == 'nt' else 'clear')
    performance.clear()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if (flagDesenhaEixos):
        global Min, Max, Meio
        Drawer.drawAxis(Min, Max, Meio)

    Drawer.displayTitle(queue[0].__name__, Min.x, Max.y)
    Drawer.displayTitle("<q> to quit, <a> to next, <s> to previous", Min.x, Min.y - 25)
    queue[0]()
    Drawer.drawPolygon(CampoDeVisao, 1, 0, 0)

    # print(f"total: {total}")
    print(f"Modo {queue[0].__name__}")
    print(f"Posi????o {pos}")
    for k, v in performance.items():
        print(f"{k}: {v}")
    print()
    
    if queue[0].__name__ == "quadTree":
        # for k, v in overhead.items():
        #     print(f"{k}: {v}")
        print(f"max-points-inside: {QTMinN}")
        print(f"bbox-precision: {10**-QTBBoxPrecision}")

    glutSwapBuffers()
    # glutPostRedisplay()


def PosicionaCampoDeVisao(n):
    global AnguloDoCampoDeVisao, PosicaoDoCampoDeVisao
    global pos
    
    pos = n
    if n == 1:
        AnguloDoCampoDeVisao = 0
        PosicaoDoCampoDeVisao = Meio
    if n == 2:
        AnguloDoCampoDeVisao = 90
        PosicaoDoCampoDeVisao = Meio
    if n == 3:
        AnguloDoCampoDeVisao = 90
        PosicaoDoCampoDeVisao = Meio*0.5
    if n == 4:
        AnguloDoCampoDeVisao = 0
        PosicaoDoCampoDeVisao = Meio + Meio*0.5

    PosicionaTrianguloDoCampoDeVisao()


def keyboard(*args):
    global flagDesenhaEixos, TamanhoCampoVisao
    global queue, QTMinN, QTRoot, QTBBoxPrecision, QTShowAll

    if args[0] == b'q' or args[0] == b'\x1b':
        os._exit(0)
    if args[0] == b's':
        queue.append(queue.pop(0))
    if args[0] == b'a':
        queue.insert(0, queue.pop())
    if args[0] == b'p':
        return print(PontosDoCenario)
    if args[0] == b'1':
        PosicionaCampoDeVisao(1)
    if args[0] == b'2':
        PosicionaCampoDeVisao(2)
    if args[0] == b'3':
        PosicionaCampoDeVisao(3)
    if args[0] == b'4':
        PosicionaCampoDeVisao(4)
    
    # QuadTree commands
    if args[0] == b'x':
        QTMinN += 1
        QTRoot = initQuadTree()
    if args[0] == b'z' and QTMinN > 1:
        QTMinN -= 1
        QTRoot = initQuadTree()
    if args[0] == b'v':
        QTBBoxPrecision += 1
        QTRoot = initQuadTree()
    if args[0] == b'c' and QTBBoxPrecision > 0:
        QTBBoxPrecision -= 1
        QTRoot = initQuadTree()
    if args[0] == b'b':
        QTShowAll = not QTShowAll 
        
    # CampoVisao commands
    if args[0] == b'.':
        TamanhoCampoVisao += .01
    if args[0] == b',':
        TamanhoCampoVisao -= .01
    if args[0] == b' ':
        flagDesenhaEixos = not flagDesenhaEixos

    PosicionaTrianguloDoCampoDeVisao()

    glutPostRedisplay()


def arrow_keys(a_keys: int, x: int, y: int):
    global AnguloDoCampoDeVisao

    #print ("Tecla:", a_keys)
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        AvancaCampoDeVisao(4)
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        AvancaCampoDeVisao(-4)
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        AnguloDoCampoDeVisao = AnguloDoCampoDeVisao + 4
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        AnguloDoCampoDeVisao = AnguloDoCampoDeVisao - 4

    PosicionaTrianguloDoCampoDeVisao()
    glutPostRedisplay()


def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    if (state != GLUT_DOWN):
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    #print ("Mouse:", x, ",", y)
    # Converte a coordenada de tela para o sistema de coordenadas do
    # universo definido pela glOrtho
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Point(
        worldCoordinate1[0], worldCoordinate1[1], worldCoordinate1[2])
    print(f"Point clicado: {str(PontoClicado)}")

    glutPostRedisplay()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str,
                        help="filepath to set of points")
    args = parser.parse_args()
    filepath = args.file

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(900, 900)

    mainWindow = glutCreateWindow("Pontos no Triangulo")
    glutDisplayFunc(display)
    init(filepath)

    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(arrow_keys)
    glutMouseFunc(mouse)

    try:
        glutMainLoop()
    except SystemExit:
        pass


if __name__ == '__main__':
    main()
