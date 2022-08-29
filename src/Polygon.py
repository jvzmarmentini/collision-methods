import copy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Point import *


class Polygon:

    def __init__(self):
        self.Vertices = []

    def __len__(self):
        return len(self.Vertices)

    def __str__(self) -> str:
        return '\n'.join([str(x) for x in self.Vertices])
    
    def insereVertice(self, x: float, y: float, z: float):
        self.Vertices.append(Point(x,y,z))

    def getVertice(self, i) -> Point:
        return copy.deepcopy(self.Vertices[i])
    
    def desenhaPoligono(self):
        glBegin(GL_LINE_LOOP)
        for V in self.Vertices:
            glVertex3f(V.x,V.y,V.z)
        glEnd();

    def desenhaVertices(self):
        glBegin(GL_POINTS);
        for V in self.Vertices:
            glVertex3f(V.x,V.y,V.z)
        glEnd();

    def getLimits(self) -> Tuple[Point]:
        Min = copy.deepcopy(self.Vertices[0])
        Max = copy.deepcopy(self.Vertices[0])

        Min.x = min([v.x for v in self.Vertices])
        Min.y = min([v.y for v in self.Vertices])
        Min.z = min([v.z for v in self.Vertices]) 

        Max.x = max([v.x for v in self.Vertices]) 
        Max.y = max([v.y for v in self.Vertices]) 
        Max.z = max([v.z for v in self.Vertices]) 
    
        return Min, Max

    def LePontosDeArquivo(self, Nome):
        
        Pt = Point()
        infile = open(Nome)
        line = infile.readline()
        number = int(line)
        for line in infile:
            words = line.split() # Separa as palavras na linha
            x = float (words[0])
            y = float (words[1])
            self.insereVertice(x,y,0)
            #Mapa.insereVertice(*map(float,line.split))
        infile.close()
        
        #print ("Após leitura do arquivo:")
        #Min.imprime()
        #Max.imprime()
        return self.getLimits()

    def getAresta(self, n):
        P1 = self.Vertices[n]
        P2 = self.Vertices[(n+1) % len(self)]
        return P1, P2

    def desenhaAresta(self, n):
        glBegin(GL_LINES)
        glVertex3f(self.Vertices[n].x,self.Vertices[n].y,self.Vertices[n].z)
        n1 = (n+1) % len(self)
        glVertex3f(self.Vertices[n1].x,self.Vertices[n1].y,self.Vertices[n1].z)
        glEnd()

    def alteraVertice(self, i, P):
        self.Vertices[i] = P
