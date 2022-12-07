import pygame, sys
from pygame.locals import *

BLACK = (0, 0, 0)

class Puerta:
    """Clase de base para puertas lógicas"""

    def __init__(self,posicionx,posiciony,tipo,ImagenPuerta,unaria):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.ImagenPuerta = ImagenPuerta
        self.unaria = unaria

        self.rect = self.ImagenPuerta.get_rect()
        self.rect.x = posicionx
        self.rect.y = posiciony
        
        self.Entradas = []
        self.Salida = False

        self.seleccionado = False
    
    def __str__(self):
        return "Puerta " + self.tipo + " : " + str(self.rect.x) + " / " + str(self.rect.y)
    
    def mover(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0]-100
        self.rect.y = mouse_pos[1]-80
    
    def mostrar(self,fondo):
        fondo.blit(self.ImagenPuerta, self.rect)
    
    def seleccionar(self):
        if self.seleccionado:
            self.seleccionado = False
        
        else:
            self.seleccionado = True


class PuertaAND(Puerta):
    """Clase para la puerta AND"""
    def __init__(self,posicionx,posiciony):
        tipo = "AND"
        ImagenPuerta = pygame.image.load("AND.png")
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        Boole = True

        for Entrada in self.Entradas:
            if Entrada == False:
                Boole = False
                break
        
        self.Salida = Boole

class PuertaOR(Puerta):
    """Clase para la puerta OR"""
    def __init__(self,posicionx,posiciony):
        tipo = "OR"
        ImagenPuerta = pygame.image.load("OR.png")
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        Boole = False

        for Entrada in self.Entradas:
            if Entrada == True:
                Boole = True
                break
        
        self.Salida = Boole

class PuertaNAND(Puerta):
    """Clase para la puerta NAND"""
    def __init__(self,posicionx,posiciony):
        tipo = "NAND"
        ImagenPuerta = pygame.image.load("NAND.png")
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        Boole = False

        for Entrada in self.Entradas:
            if Entrada == False:
                Boole = True
                break
        
        self.Salida = Boole

class PuertaNOR(Puerta):
    """Clase para la puerta NOR"""
    def __init__(self,posicionx,posiciony):
        tipo = "NOR"
        ImagenPuerta = pygame.image.load("NOR.png")
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        Boole = True

        for Entrada in self.Entradas:
            if Entrada == True:
                Boole = False
                break
        
        self.Salida = Boole

class PuertaXOR(Puerta):
    """Clase para la puerta XOR"""
    def __init__(self,posicionx,posiciony):
        tipo = "XOR"
        ImagenPuerta = pygame.image.load("XOR.png")
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        #Devuelve TRUE si el número de entradas TRUE es impar (generador de paridad)
        Unos = 0

        for Entrada in self.Entradas:
            if Entrada == True:
                Unos += 1

        if (unos % 2 == 1 and unos != 0):
            self.Salida = True
        else:
            self.Salida = False

class PuertaXNOR(Puerta):
    """Clase para la puerta XNOR"""
    def __init__(self,posicionx,posiciony):
        tipo = "XNOR"
        ImagenPuerta = pygame.image.load("XNOR.png")
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        #Devuelve TRUE si el número de entradas TRUE es impar (generador de paridad)
        Unos = 0

        for Entrada in self.Entradas:
            if Entrada == True:
                Unos += 1

        if (unos % 2 == 1 and unos != 0):
            self.Salida = False
        else:
            self.Salida = True

class PuertaNOT(Puerta):
    """Clase para la puerta NOT"""
    def __init__(self,posicionx,posiciony):
        tipo = "NOT"
        ImagenPuerta = pygame.image.load("NOT.png")
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = True)
        self.Entrada = self.Entradas[0]

    def logica(self):
        Boole = True

        if self.Entrada and (self.Entrada == True):
            Boole = False
            
        self.Salida = Boole