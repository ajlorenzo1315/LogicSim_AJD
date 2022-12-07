import pygame, sys
from pygame.locals import *

class PuertaAND:
    """Clase de prueba para la puerta AND"""

    def __init__(self,posicionx,posiciony):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenPuertaAND = pygame.image.load("AND.png")

        self.rect = self.ImagenPuertaAND.get_rect()
        self.rect.x = posicionx
        self.rect.y = posiciony

        self.Entradas = {}
        self.Salida = False

        self.seleccionado = False
    
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
        for Entrada in Entradas:
            if Entrada == False:
                self.Salida = False
                break

        self.Salida = True

class Pin:
    """Clase para los pines de entrada. Con clic se pueden activar o desactivar"""

    """Falta por añadir el sprite para poder alternar entre imagenes de 0 y 1"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenPin = pygame.image.load("AND.png")

        self.rect = self.ImagenPin.get_rect()
        self.rect.x = 30
        self.rect.y = 30

        self.Estado = False

        self.seleccionado = False
    
    def mover(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0]-100
        self.rect.y = mouse_pos[1]-80
    
    def mostrar(self,fondo):
        fondo.blit(self.ImagenPin, self.rect)
    
    def seleccionar(self):
        if self.seleccionado:
            self.seleccionado = False
        
        else:
            self.seleccionado = True
    
    def logica(self,Entradas):
        if self.Estado:
            self.Estado = False
        
        else:
            self.Estado = True
        
def Prueba():
    pygame.init()
    Ventana = pygame.display.set_mode((861,460))

    Fondo2 = pygame.image.load("Fondo2.png")

    Componentes = {}

    pygame.display.set_caption("LogicSim (totally not a copy)")

    i = 0
    AlgoSeleccionado = False
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
                    
        Ventana.blit(Fondo2, (0,0))
        for Componente in Componentes.values():
            Componente.mostrar(Ventana)
        
        pygame.display.update()
        
Prueba()