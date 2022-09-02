# -*- coding: utf-8 -*-
import copy
import os
import random
import numpy as np

from anytree import Node, RenderTree, PreOrderIter
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
QuadTreeRoot = Node('n')

AnguloDoCampoDeVisao = 0.0

Min = Point()
Max = Point()
Meio = Point()
Tamanho = Point()
TamanhoCampoVisao = .25

PontoClicado = Point()

flagDesenhaEixos = True


def raw():
    Drawer.drawPoints(PontosDoCenario, 0, 0, 1)


def bruteForce():
    for p in PontosDoCenario.Vertices:
        if CampoDeVisao.isPointInside(p):
            Drawer.drawPoint(p, 0, 1, 0)
        else:
            Drawer.drawPoint(p, 1, 0, 0)


def envelope():
    Drawer.drawBBox(BBox.Vertices, 0, 1, 1)

    for p in PontosDoCenario.Vertices:
        if BBox.isPointInsideBox(p):
            Drawer.drawPoint(p, 1, 0, 0)
        else:
            if CampoDeVisao.isPointInside(p):
                Drawer.drawPoint(p, 0, 1, 0)
            else:
                Drawer.drawPoint(p, 1, 1, 0)


def _initQuadTree(gmin: Point, gmax: Point, parent: Node, points: List[Point]) -> None:
    alp = ['a', 'b', 'c', 'd']

    mid = (gmin + gmax) * .5
    delta = mid - gmin

    for s in [0, 1]:
        for c in [0, 1]:
            name = parent.name + alp.pop(0)
            lmin = Point(gmin.x + c * delta.x, gmin.y + s * delta.y)
            lmax = Point(mid.x + c * delta.x, mid.y + s * delta.y)
            poly = Polygon(lmin, lmax)

            inside = list(filter(lambda p: not poly.isPointInsideBox(p), points))

            node = Node(name=name, poly=poly, parent=parent, inside=inside)
            if node.depth < 4:
                _initQuadTree(lmin, lmax, node, inside)

def quadTree():
    global Min, Max, BBox
    points = copy.deepcopy(PontosDoCenario.Vertices)
    root = Node("q", poly=Polygon(Min, Max), inside=points)

    _initQuadTree(Min, Max, root, points)

    for pre, _, node in RenderTree(root):
        # print(f"{pre}{node.name}, min=[{node.poly.Vertices[0]}] | max=[{node.poly.Vertices[1]}]")
        # Drawer.drawBBox(node.poly.Vertices, 0, 1, 1)
        color = list(np.random.uniform(1,0,3))
        Drawer.drawListPoints(node.inside, *color)

    for leafNode in PreOrderIter(root, filter_=lambda n: n.is_leaf):
        bbox = leafNode.poly
        if BBox.collisionWithBBox(bbox):
            Drawer.drawBBox(bbox.Vertices, 0, 1, 1)

    # DotExporter(root).to_picture("assets/root.png")


queue = [quadTree, envelope , raw, bruteForce]


def GeraPontos(qtd, Min: Point, Max: Point):
    global PontosDoCenario
    Escala = Point()
    Escala = (Max - Min) * (1.0/1000.0)

    for _ in range(qtd):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        x = x * Escala.x + Min.x
        y = y * Escala.y + Min.y
        P = Point(x, y)
        PontosDoCenario.insertVertice(P)


def readFromFile(filepath: str) -> None:
    with open(filepath) as f:
        for line in f:
            words = line.split()
            x = float(words[0])
            y = float(words[1])
            PontosDoCenario.insereVertice(x, y, 0.0)


def CriaTrianguloDoCampoDeVisao():
    global TrianguloBase, CampoDeVisao

    vetor = Point(1.0, 0.0, 0.0)
    TrianguloBase.insertVertice(0.0, 0.0, 0.0)
    CampoDeVisao.insertVertice(0.0, 0.0, 0.0)

    vetor.rotacionaZ(45)
    TrianguloBase.insertVertice(vetor.x, vetor.y, vetor.z)
    CampoDeVisao.insertVertice(vetor.x, vetor.y, vetor.z)

    vetor.rotacionaZ(-90)
    TrianguloBase.insertVertice(vetor.x, vetor.y, vetor.z)
    CampoDeVisao.insertVertice(vetor.x, vetor.y, vetor.z)


def PosicionaTrianguloDoCampoDeVisao():
    global Tamanho, CampoDeVisao, PosicaoDoCampoDeVisao, TrianguloBase
    global AnguloDoCampoDeVisao, TamanhoCampoVisao

    tam = Tamanho.x * TamanhoCampoVisao
    for i in range(len(TrianguloBase)):
        temp = TrianguloBase.getVertice(i).rotacionaZ(AnguloDoCampoDeVisao)
        CampoDeVisao.modifyVertice(i, PosicaoDoCampoDeVisao + temp*tam)

    min, max = CampoDeVisao.getLimits()
    BBox.modifyVertice(0, min)
    BBox.modifyVertice(1, max)


def AvancaCampoDeVisao(distancia):
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao
    vetor = Point(1, 0, 0)
    vetor.rotacionaZ(AnguloDoCampoDeVisao)
    PosicaoDoCampoDeVisao = PosicaoDoCampoDeVisao + vetor * distancia


def init():
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao
    global Min, Max, Meio, Tamanho

    # Define a cor do fundo da tela (AZUL)
    glClearColor(0, 0, 0, 1)

    GeraPontos(1000, Point(0, 0), Point(500, 500))
    Min, Max = PontosDoCenario.getLimits()
    #Min, Max = PontosDoCenario.LePontosDeArquivo("PoligonoDeTeste.txt")

    Meio = (Max+Min) * 0.5  # Point central da janela
    Tamanho = (Max - Min)  # Tamanho da janela em X,Y

    # Ajusta variaveis do triangulo que representa o campo de visao
    PosicaoDoCampoDeVisao = Meio
    AnguloDoCampoDeVisao = 0

    # Cria o triangulo que representa o campo de visao
    CriaTrianguloDoCampoDeVisao()

    min, max = CampoDeVisao.getLimits()
    BBox.insertVertice(min)
    BBox.insertVertice(max)

    PosicionaTrianguloDoCampoDeVisao()


def reshape(w, h):
    global Min, Max

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    global flagDesenhaEixos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if (flagDesenhaEixos):
        global Min, Max, Meio
        Drawer.drawAxis(Min, Max, Meio)

    queue[0]()

    glLineWidth(3)
    Drawer.drawPolygon(CampoDeVisao, 1, 0, 0)

    glutSwapBuffers()
    # glutPostRedisplay()


def keyboard(*args):
    global flagDesenhaEixos, TamanhoCampoVisao
    global queue

    # If escape is pressed, kill everything.
    if args[0] == b'q' or args[0] == b'\x1b':
        os._exit(0)
    if args[0] == b'w':
        queue.append(queue.pop(0))
    if args[0] == b'p':
        print(PontosDoCenario)
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
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    # Define o tamanho inicial da janela grafica do programa
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    wind = glutCreateWindow("Pontos no Triangulo")
    glutDisplayFunc(display)
    # glutIdleFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(arrow_keys)
    glutMouseFunc(mouse)
    init()

    try:
        glutMainLoop()
    except SystemExit:
        pass


if __name__ == '__main__':
    main()

