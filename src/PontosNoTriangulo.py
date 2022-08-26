# -*- coding: utf-8 -*-
import os
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
import random

PontosDoCenario = Polygon()
CampoDeVisao = Polygon()
TrianguloBase = Polygon()
PosicaoDoCampoDeVisao = Ponto

AnguloDoCampoDeVisao=0.0

Min = Ponto()
Max = Ponto()
Tamanho = Ponto()
Meio = Ponto()

PontoClicado = Ponto()

flagDesenhaEixos = True

paintPoints = False
paintOtimization = False


def vetProd(v1,v2):
    return v1.x * v2.y - v1.y * v2.x


def raw():
    glPointSize(5)
    PontosDoCenario.desenhaVertices()

def bruteForce():
    cPoints = [None] * 3
    cVet = [None] * 3

    for n in range(len(CampoDeVisao)):
        cPoints[n], p2 = CampoDeVisao.getAresta(n)
        cVet[n] = p2 - cPoints[n]

    for p in PontosDoCenario.Vertices:
        prod = [None] * 3

        for n in range(len(CampoDeVisao)):
            pVet = p - cPoints[n]
            prod[n] = vetProd(cVet[n], pVet)
        

        glPointSize(5)
        glBegin(GL_POINTS)
        if all(n >= 0 for n in prod) or all(n < 0 for n in prod):
            glColor3f(0, 1, 0)
        else:
            glColor3f(1,0,0)
        glVertex3f(p.x,p.y,p.z)
        glEnd()



def envelope():
    print("envelope")

def quadTree():
    print("quadtree")

queue = [raw, bruteForce, envelope, quadTree]


# **********************************************************************
# GeraPontos(int qtd)
#      Metodo que gera pontos aleatorios no intervalo [Min..Max]
# **********************************************************************
def GeraPontos(qtd, Min: Ponto, Max: Ponto):
    global PontosDoCenario
    Escala = Ponto()
    Escala = (Max - Min) * (1.0/1000.0)
    
    for i in range(qtd):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        x = x * Escala.x + Min.x
        y = y * Escala.y + Min.y
        P = Ponto(x,y)
        PontosDoCenario.insereVertice(P.x, P.y, P.z)
        #PontosDoCenario.insereVertice(P)

# **********************************************************************
#  CriaTrianguloDoCampoDeVisao()
#  Cria um triangulo a partir do vetor (1,0,0), girando este vetor
#  em 45 e -45 graus.
#  Este vetor fica armazenado nas variáveis "TrianguloBase" e
#  "CampoDeVisao"
# **********************************************************************
def CriaTrianguloDoCampoDeVisao():
    global TrianguloBase, CampoDeVisao

    vetor = Ponto(1,0,0)

    TrianguloBase.insereVertice(0,0,0)
    CampoDeVisao.insereVertice(0,0,0)
    
    vetor.rotacionaZ(45)
    TrianguloBase.insereVertice (vetor.x,vetor.y, vetor.z)
    CampoDeVisao.insereVertice (vetor.x,vetor.y, vetor.z)
    
    vetor.rotacionaZ(-90)
    TrianguloBase.insereVertice (vetor.x,vetor.y, vetor.z)
    CampoDeVisao.insereVertice (vetor.x,vetor.y, vetor.z)


# ***********************************************************************************
# void PosicionaTrianguloDoCampoDeVisao()
#  Posiciona o campo de visão na posicao PosicaoDoCampoDeVisao,
#  com a orientacao "AnguloDoCampoDeVisao".
#  O tamanho do campo de visão eh de 25% da largura da janela.
# **********************************************************************
def PosicionaTrianguloDoCampoDeVisao():
    global Tamanho, CampoDeVisao, PosicaoDoCampoDeVisao, TrianguloBase
    global AnguloDoCampoDeVisao


    tam = Tamanho.x * 0.25
    temp = Ponto()
    for i in range(len(TrianguloBase)):
        temp = TrianguloBase.getVertice(i)
        temp.rotacionaZ(AnguloDoCampoDeVisao)
        CampoDeVisao.alteraVertice(i, PosicaoDoCampoDeVisao + temp*tam)


def AvancaCampoDeVisao(distancia):
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao
    vetor = Ponto(1,0,0)
    vetor.rotacionaZ(AnguloDoCampoDeVisao)
    PosicaoDoCampoDeVisao = PosicaoDoCampoDeVisao + vetor * distancia

# ***********************************************************************************
#
# ***********************************************************************************
def init():
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao

    # Define a cor do fundo da tela (AZUL)
    glClearColor(0, 0, 1, 1)
    global Min, Max, Meio, Tamanho

    GeraPontos(1000, Ponto(0,0), Ponto(500,500))
    Min, Max = PontosDoCenario.getLimits()
    #Min, Max = PontosDoCenario.LePontosDeArquivo("PoligonoDeTeste.txt")

    Meio = (Max+Min) * 0.5 # Ponto central da janela
    Tamanho = (Max - Min) # Tamanho da janela em X,Y

    # Ajusta variaveis do triangulo que representa o campo de visao
    PosicaoDoCampoDeVisao = Meio
    AnguloDoCampoDeVisao = 0

    # Cria o triangulo que representa o campo de visao
    CriaTrianguloDoCampoDeVisao()
    PosicionaTrianguloDoCampoDeVisao()
    
# ***********************************************************************************
#
# ***********************************************************************************
def DesenhaLinha (P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ***********************************************************************************
#
# ***********************************************************************************
def DesenhaEixos():
    global Min, Max, Meio

    glBegin(GL_LINES)
    # eixo horizontal
    glVertex2f(Min.x,Meio.y)
    glVertex2f(Max.x,Meio.y)
    # eixo vertical
    glVertex2f(Meio.x,Min.y)
    glVertex2f(Meio.x,Max.y)
    glEnd()

# ***********************************************************************************
def reshape(w,h):
    global Min, Max

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ***********************************************************************************
def display():
    global PontoClicado, flagDesenhaEixos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1.0, 1.0, 0.0)

    if (flagDesenhaEixos):
        glLineWidth(1)
        glColor3f(1,1,1); # R, G, B  [0..1]
        DesenhaEixos()

    queue[0]()

    glLineWidth(3)
    glColor3f(1,0,0) # R, G, B  [0..1]
    CampoDeVisao.desenhaPoligono()

    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
def keyboard(*args):
    global flagDesenhaEixos

    global queue

    # If escape is pressed, kill everything.
    if args[0] == b'q' or args[0] == b'\x1b':
        os._exit(0)
    if args[0] == b'w':
        queue.append(queue.pop(0))
    if args[0] == b'e':
        not paintPoints
    if args[0] == b'r':
        not paintOtimization
    if args[0] == b'p':
        PontosDoCenario.imprimeVertices()
    if args[0] == b'1':
        P1.imprime()
        P2.imprime()
    if args[0] == b' ':
        flagDesenhaEixos = not flagDesenhaEixos

    # Forca o redesenho da tela
    glutPostRedisplay()
# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    global AnguloDoCampoDeVisao, TrianguloBase

    #print ("Tecla:", a_keys)
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        AvancaCampoDeVisao(2)
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        AvancaCampoDeVisao(-2)
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        AnguloDoCampoDeVisao = AnguloDoCampoDeVisao + 2
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        AnguloDoCampoDeVisao = AnguloDoCampoDeVisao - 2

    PosicionaTrianguloDoCampoDeVisao()

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
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

    PontoClicado = Ponto (worldCoordinate1[0],worldCoordinate1[1], worldCoordinate1[2])
    PontoClicado.imprime("Ponto Clicado:")

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouseMove(x: int, y: int):
    #glutPostRedisplay()
    return


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Pontos no Triangulo")
glutDisplayFunc(display)
#glutIdleFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_keys)
glutMouseFunc(mouse)
init()

try:
    glutMainLoop()
except SystemExit:
    pass
