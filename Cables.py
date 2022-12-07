import pygame, sys
from pygame.locals import *

BLACK = (0, 0, 0)


class PuertaAND:
    """Clase de prueba para la puerta AND"""

    def __init__(self,posicionx,posiciony):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenPuertaAND = pygame.image.load("AND.png")

        self.rect = self.ImagenPuertaAND.get_rect()
        self.rect.x = posicionx
        self.rect.y = posiciony

        self.Entradas = []
        self.Salida = False

        self.seleccionado = False
    
    def __str__(self):
        return "Puerta AND: " + str(self.rect.x) + " / " + str(self.rect.y)
    
    def mover(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0]-100
        self.rect.y = mouse_pos[1]-80
    
    def mostrar(self,fondo):
        fondo.blit(self.ImagenPuertaAND, self.rect)
    
    def seleccionar(self):
        if self.seleccionado:
            self.seleccionado = False
        
        else:
            self.seleccionado = True
    
    def logica(self,Entradas):

        Boole = True

        if Entradas:
            for Entrada in Entradas:
                if Entrada == False:
                    Boole = False
                    break
        
        self.Salida = Boole


class Cable():
    def __init__(self,ID):
        self.ID = ID
        self.color = BLACK
        self.grosor = 4
        self.conexion = False
        self.inicio = None
        self.final = None
    
    def conectar(self,elemento1,elemento2):
        elemento2.Entradas.append(elemento1)
        self.conexion = True
        self.inicio = elemento1
        self.final = elemento2
    
    def graficar(self,elemento1,elemento2):
        inicio = elemento1.rect.midright
        final = elemento2.rect.midleft

        self.conectar(elemento1,elemento2)

        pygame.draw.line(Fondo2, self.color, inicio, final, self.grosor)
    
    def actualizar(self):
        self.graficar(self.inicio,self.final)
    
    def borrar_conexiones(self):
        self.final.Entradas.remove(self.inicio)

def Prueba():
    global Ventana, Fondo2

    pygame.init()
    Ventana = pygame.display.set_mode((861,460))

    Fondo2 = pygame.image.load("Fondo2.png")

    Componentes = {}
    Cables = []

    pygame.display.set_caption("LogicSim (totally not a copy)")

    i = 0
    AlgoSeleccionado = False
    Cableando = False
    In = None
    Out = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                # Set the x, y postions of the mouse click
                x, y = event.pos
                for Componente in Componentes.values():
                    if Componente.rect.collidepoint(x, y):
                        if Cableando:
                            if not In:
                                print("Seleccionado el primer componente: " + str(Componente))
                                In = Componente
                                
                            
                            elif not Out:
                                print("Seleccionado el segundo componente: " + str(Componente))
                                Out = Componente
                                

                        else:
                            print('Objeto seleccionado')
                            Componente.seleccionar()
                            AlgoSeleccionado = not AlgoSeleccionado
                    
            elif (event.type == pygame.MOUSEMOTION):
                for Componente in Componentes.values():
                    if Componente.seleccionado:
                        print("Moviendo...")
                        Componente.mover()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:
                    print("Se pulsó la tecla A")
                    mouse_pos = pygame.mouse.get_pos()
                    Componentes[i] = PuertaAND(mouse_pos[0]-100,mouse_pos[1]-80)
                    i += 1
                
                if event.key == pygame.K_c:
                    if not Cableando:
                        print("Comienza el cableado")
                        Cableando = True
                    else:
                        print("Se detuvo el cableado")
                        Cableando = False
                        In = None
                        Out = None
                
                if event.key == pygame.K_j and Cableando:
                    if In and Out:
                        print("Unidos")
                        placeholder = Cable(i)
                        Cables.append(placeholder)
                        placeholder.graficar(In,Out)
                        In = None
                        Out = None
                        Cableando = False
                
                if event.key == pygame.K_SPACE:
                    print("Borrar Cables")
                    Fondo2 = pygame.image.load("Fondo2.png")
                    for wire in Cables:
                        wire.borrar_conexiones()
                    Cables = []
                
        Ventana.blit(Fondo2, (0,0))
        for Componente in Componentes.values():
            Componente.mostrar(Ventana)
        
        pygame.display.update()
        
Prueba()