####################################################################
# By Juan Daniel Suárez  and  Alicia Jiajun Lorenzo
# 26/06/2020
#
# Logi AJD file (MAIN PROGRAM)

####################################################################


try:
   import pygame 
   from tkinter import *
   from tkinter import messagebox
   from tkinter.filedialog import askopenfilename, asksaveasfilename
   from win32api import GetSystemMetrics
   from pygame.locals import *
   import  os
   from tkinter.ttk import *
   import time
except:
   import install_requirements
   import pygame 
   from tkinter import *
   from tkinter import messagebox
   from pygame.locals import *
   from tkinter.filedialog import askopenfilename, asksaveasfilename
   from win32api import GetSystemMetrics
   import os
   from tkinter.ttk import *
   import time
import sys

class App(Frame):
 
    def __init__(self, parent,Elementos):
        Frame.__init__(self, parent)
        self.CreateUI()
        self.LoadTable(Elementos)
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)
 
    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('ID', 'Tipo', 'Estado')
        tv.heading("#0", text='Nombre', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('ID', text='ID')
        tv.column('ID', anchor='center', width=100)
        tv.heading('Tipo', text='Tipo')
        tv.column('Tipo', anchor='center', width=100)
        tv.heading('Estado', text='Estado')
        tv.column('Estado', anchor='center', width=100)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
 
    def LoadTable(self,Elementos):
        for Clave, Elemento in Elementos.items():
            self.treeview.insert('', 'end', text="WIP", values=(str(Clave),Elemento.tipo,str(Elemento.Salida)))

class Cell(object):
    #celda (usado en el grid cada cuadrito)
    def __init__(self, size, color=[0, 0, 0]):
        self.size = size
        self.color = color
        self.subsurface = pygame.Surface((self.size,self.size))
        self.subsurface.fill(self.color)
        self.pos = (0, 0)

    def change_color(self, color):
        self.color = color
        self.subsurface.fill(self.color)

    def Draw(self, win, x, y):
        self.pos = (x, y)
        win.blit(self.subsurface, self.pos)

class Grid(object):
    def __init__(self, xc, yc, csize, x, y, color=[255, 255, 255]):
        self.xCount = xc
        self.yCount = yc
        self.cellSize = csize
        self.pos = (x, y)
        self.color = color
        self.grid = []
        self.undoList = [[], []]

        for i in range(self.xCount):
            self.grid.append([])
            self.undoList[0].append([])
            self.undoList[1].append([])
            for j in range(self.yCount):
                self.grid[i].append(Cell(self.cellSize, self.color))
                self.undoList[0][i].append(self.color)
                self.undoList[1][i].append(self.color)

    def Draw(self, win):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].Draw(win, self.pos[0]+(self.cellSize*i), self.pos[1]+(self.cellSize*j))

    def change_color(self, posx, posy, color):
        self.grid[posy][posx].change_color(color)

    def change_color_all(self,color):
        self.color=color
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].change_color(self.color)

    def clean(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].change_color(self.color)

class Button(object):
    active = False
    clicked = False
    rollOver = False
    def __init__(self, posX, posY, width, height, color, text="Button", type=1, fontSize=25, fontColor=(0, 0, 0)):
        self.pos = [posX, posY]
        self.drawPos = self.pos.copy()
        self.width, self.height = width, height
        self.color = color
        self.text, self.fontSize, self.fontColor = text, fontSize, fontColor
        self.type = type
        self.subsurface = pygame.Surface((self.width, self.height))
        self.subsurface.fill(self.color)
        self.font = pygame.font.SysFont(None, self.fontSize)
        self.mes = self.font.render(self.text, True, self.fontColor)
        self.slideVal = 0

    def Draw(self, win, val=-1):
        if self.type == 1:
            if self.rollOver and not self.clicked:
                self.subsurface.set_alpha(100)
            else:
                self.subsurface.set_alpha(150)
            
            if self.clicked:
                self.subsurface.set_alpha(255)
            
            win.blit(self.subsurface, self.pos)
            self.subsurface.blit(self.mes, (15, self.height/3))
        elif self.type == 2:
            self.slideVal = Remap(-60,60,1,5,(self.pos[0]- self.drawPos[0]))
            pygame.draw.rect(screen, (190,190,190), (self.drawPos[0]-100, self.drawPos[1]-30, 168, 60))
            pygame.draw.rect(screen, (140,140,140), (self.drawPos[0]-60, self.drawPos[1]+self.height/3, 120, self.height/2))
            pygame.draw.rect(screen, (220,220,220), (self.drawPos[0]-90, self.drawPos[1]+1, 20, 20))
            self.valMes = self.font.render(str(val), True, (30,30,30))
            win.blit(self.valMes, (self.drawPos[0]-85, self.drawPos[1]+3))
            win.blit(self.subsurface, (self.pos[0]-self.width/2, self.pos[1]))
            win.blit(self.mes, (self.drawPos[0]-90, self.drawPos[1]-25))

    def chage_name(self,text="Button", fontSize=25, fontColor=(0, 0, 0)):
        self.text, self.fontSize, self.fontColor = text, fontSize, fontColor
        self.font = pygame.font.SysFont(None, self.fontSize)
        self.mes = self.font.render(self.text, True, self.fontColor)


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
        
        self.Salidaes_puertas={}
        self.Entradas = {}
        self.Siguiente = {}
        self.Salida = False

        

        self.seleccionado = False
    
    def __str__(self):
        return "Puerta " + self.tipo + " : " + str(self.rect.x) + " / " + str(self.rect.y)
    
    def mover(self):
        #x,y=self.rect.center
        #print(x,y)
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center=mouse_pos
        #self.rect.x = mouse_pos[0]-100
        #self.rect.y = mouse_pos[1]-80
    
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
        ImagenPuerta.set_colorkey((255,255,255))
        # return a width and height of an image

        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image

        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        Boole = True

        for Entrada in self.Entradas.values():
            if Entrada.Salida == False:
                Boole = False
                break
        
        self.Salida = Boole
    

class PuertaOR(Puerta):
    """Clase para la puerta OR"""
    def __init__(self,posicionx,posiciony):
        tipo = "OR"
        ImagenPuerta = pygame.image.load("OR.png")
        ImagenPuerta.set_colorkey((255,255,255))
        # return a width and height of an image

        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image

        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        Boole = False

        for Entrada in self.Entradas.values():
            if Entrada.Salida == True:
                Boole = True
                break
        
        self.Salida = Boole

class PuertaNAND(Puerta):
    """Clase para la puerta NAND"""
    def __init__(self,posicionx,posiciony):
        tipo = "NAND"
        ImagenPuerta = pygame.image.load("NAND.png")
        ImagenPuerta.set_colorkey((255,255,255))
        # return a width and height of an image

        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image

        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        Boole = False

        for Entrada in self.Entradas.values():
            if Entrada.Salida == False:
                Boole = True
                break
        
        self.Salida = Boole

class PuertaNOR(Puerta):
    """Clase para la puerta NOR"""
    def __init__(self,posicionx,posiciony):
        tipo = "NOR"
        ImagenPuerta = pygame.image.load("NOR.png")
        ImagenPuerta.set_colorkey((255,255,255))
        # return a width and height of an image

        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image

        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        Boole = True

        for Entrada in self.Entradas.values():
            if Entrada.Salida == True:
                Boole = False
                break
        
        self.Salida = Boole

class PuertaXOR(Puerta):
    """Clase para la puerta XOR"""
    def __init__(self,posicionx,posiciony):
        tipo = "XOR"
        ImagenPuerta = pygame.image.load("XOR.png")
        ImagenPuerta.set_colorkey((255,255,255))
        # return a width and height of an image

        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image

        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        # draw bigger image to screen at x=100 y=100 position

        
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)
        

    def logica(self):
        #Devuelve TRUE si el número de entradas TRUE es impar (generador de paridad)
        Unos = 0

        for Entrada in self.Entradas.values():
            if Entrada.Salida == True:
                Unos += 1

        if (unos % 2 == 1 and unos != 0):
            self.Salida = True
        else:
            self.Salida = False

class PuertaXNOR(Puerta):
    """Clase para la puerta XNOR"""
    def __init__(self,posicionx,posiciony):
        tipo = "XNOR"
        ImagenPuerta = pygame.image.load("XNOR.png").convert()
        ImagenPuerta.set_colorkey((255,255,255))
        # return a width and height of an image

        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image

        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        # draw bigger image to screen at x=100 y=100 position

        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = False)

    def logica(self):
        #Devuelve TRUE si el número de entradas TRUE es impar (generador de paridad)
        Unos = 0

        for Entrada in self.Entradas.values():
            if Entrada.Salida == True:
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
        ImagenPuerta.set_colorkey((255,255,255))
        # return a width and height of an image

        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image

        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        # draw bigger image to screen at x=100 y=100 position
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = True)
        #self.Entrada = self.Entradas[0]
        self.Entradas = {}
        self.Siguiente = {}
        self.lleno=False

    def logica(self):
        Boole = True

        if self.Entrada and (self.Entrada == True):
            Boole = False
            
        self.Salida = Boole


class PinIN(Puerta):
    """Clase para el PIN"""
    def __init__(self,posicionx,posiciony):
        tipo="PinIN"
        ImagenPuerta = pygame.image.load("PININ1.png")
        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image

        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = True)

        self.Siguiente = {}
        self.lleno=False
 
    def cambio(self):
        if self.Salida:
            self.ImagenPuerta = pygame.image.load("PININ2.png")
            self.size = self.ImagenPuerta.get_size()
            # create a 2x bigger image than self.image
            self.ImagenPuerta = pygame.transform.scale(self.ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
            self.Salida = True
        
        else:
            self.ImagenPuerta = pygame.image.load("PININ1.png")
            self.size = self.ImagenPuerta.get_size()
            # create a 2x bigger image than self.image
            self.ImagenPuerta = pygame.transform.scale(self.ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
            self.Salida = False

    def logica(self):
        for Siguiente in self.Siguiente.values():
            Siguiente.Valores_puertas[self]=self.Salida
 
class PinOUT(Puerta):
    """Clase para el PIN"""
    def __init__(self,posicionx,posiciony,entrada=True):
        tipo="PinOUT"
        ImagenPuerta = pygame.image.load("PINOUT1.png")
        self.size = ImagenPuerta.get_size()
        # create a 2x bigger image than self.image
        ImagenPuerta = pygame.transform.scale(ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
        super().__init__(posicionx,posiciony,tipo,ImagenPuerta,unaria = True)

        #self.Entrada = self.Entradas[0]
        self.Entradas = {}
        self.Siguiente = {}
        self.lleno=False
 
    def logica(self):

        els = list(self.Entradas.values())
        cable = list(self.Entradas.keys())
        if els[0].Salida==True:
            self.Salida=True  
        else:
            self.Salida=False
        """els=list(self.Salidaes_puertas.values())
        cable = list(self.Entradas.keys())"""
        if self.Salida == False:
            self.ImagenPuerta = pygame.image.load("PINOUT1.png")
            self.size = self.ImagenPuerta.get_size()
            # create a 2x bigger image than self.image
            self.ImagenPuerta = pygame.transform.scale(self.ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
            
        else:
            self.ImagenPuerta = pygame.image.load("PINOUT2.png")
            self.size = self.ImagenPuerta.get_size()
            # create a 2x bigger image than self.image
            self.ImagenPuerta = pygame.transform.scale(self.ImagenPuerta, (int(self.size[0]/4), int(self.size[1]/4)))
            

class Cable():
    def __init__(self,ID):
        
        self.ID = ID
        self.color =(0, 0, 0)
        self.grosor = 4
        self.conexion = False
        self.inicio = None
        self.final = None
        self.seleccionado=False

    def __str__(self):

        return "Cable " + str(self.ID) 

    def conectar(self,elemento1,elemento2):
        elemento2.Entradas[self]=elemento1
        elemento1.Siguiente[self]=elemento2
        self.conexion = True
        self.inicio = elemento1
        self.final = elemento2
    
    def graficar(self,elemento1,elemento2,screen):
        if elemento1.Salida:
            self.color=(255,0,0)
        else:
            self.color=(0,0,0)
        inicio = elemento1.rect.midright
        final = elemento2.rect.midleft

        #print(inicio,final)
        
        self.conectar(elemento1,elemento2)
        mitadx=[inicio[0]+(final[0]-inicio[0])/2,final[0]]
        self.line=[]
        self.line.append(pygame.draw.line(screen, self.color, inicio,(mitadx[0],inicio[1]), self.grosor))
        self.line.append(pygame.draw.line(screen, self.color, (mitadx[0],inicio[1]),(mitadx[0],final[1]), self.grosor))
        self.line.append(pygame.draw.line(screen, self.color, (mitadx[0],final[1]),final, self.grosor))

    def Colisiona(self,possition):
        x, y = possition  
        for J in self.line:
            if J.collidepoint(x, y):
                return True
        

    def mostrar(self,screen):
        self.line(screen)
    
    def actualizar(self):
        self.graficar(self.inicio,self.final)
    
    def borrar_conexiones(self):
        self.final.Entradas.pop(self)
        self.inicio.Siguiente.pop(self)

class LogAJD():
    def __init__(self, Ws = GetSystemMetrics(0), Hs = GetSystemMetrics(1)):
        
        W = 700
        H = 600
        
        #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (Ws/21.5,Hs/5.25)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        self.Maximizar=True
        sys.setrecursionlimit(1000)
        self.screensize = [Ws, Hs]
        self.y_origen = 100
        self.delta_y = 100
        #desplazamiento a mayores si lo queremos
        self.offset = [0, 0]
        self.separacion = 6 #numero mas alto es menos separacion
        self.screen = None
        self.ayuda = False
        #lienzo
        self.workspace = None
        #puertas y pines
        self.Componentes = {}
        self.Cables = {}
        #todos los componentes
        self.Todos = {}
        self.Borrar=False
        #para la logica 
        self.Ejecutar=False
        #pines
        self.Pines={}
        #Una solo entrada
        self.Una_solo_entrada={}

    def graficar(self):
        BLACK = (0, 0, 0)
        pygame.init()
        #scrolling = False
        self.elemento_borrado=None
        #self.icono=pygame.display.set_icon(pygame.image.load("icono.png"))
        self.icono=pygame.display.set_icon(pygame.image.load("dragon.png"))
        self.logo=pygame.transform.scale(pygame.image.load("LOGO1.png"), (140,40))
        sw,sh=self.screensize
        colorTitleFont = pygame.font.SysFont(None, 25)
        pygame.display.set_caption("LOG AJD ")
        colorTitle = colorTitleFont.render("Color Palette", True, (50,50,50))
        #self.screen = pygame.display.set_mode(self.screensize, pygame.RESIZABLE) #de esta manera la pantalla puede agrandarse o encojerse
        self.screen=pygame.display.set_mode(self.screensize)
        #self.screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen.fill((255,255, 255))
        #print(850-12*64)
        #print(int(64*sh/850))
        #print(int(68*sw/950))
        #print(int((950-160)/12))

        fileFont = pygame.font.SysFont(None, 20)
        alto=int(sh/12)
        ancho=int((sw-109)/12)
        #print(alto,ancho)
        # es el espacio de trabajo 
        self.workspace = Grid(ancho,alto,12, 0, 0, [0, 255, 255])
        selected=0
        listo = False
        b_ancho=int(112*sh/700)
        #print(b_ancho)
        b_alto=int(29*sw/600)
        #print(b_alto)
        if sh/700>1:
            b_ancho=112
        if sw/600>1:
            b_alto=29
        #posicion de los botones 
        positon_bootoms=[sw-130,40,b_ancho,b_alto]
        distancia=b_alto+10
        #para minimizar los botoes
        Bootoms=True
       
        if Bootoms:
            #botones (100,100,100) caja (255,255,255) texto dentro de la caja
            exit_b = Button(positon_bootoms[0],positon_bootoms[1],positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "Exit", 1, 24, (255,255,255))
            eje_b = Button(positon_bootoms[0],positon_bootoms[1]+distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Ejecutar", 1, 24, (255,255,255))
           
            SL_Buttons = [exit_b, eje_b]

            #botones (100,100,100) caja (255,255,255) texto dentro de la caja
            p_and= Button(positon_bootoms[0],positon_bootoms[1]+4*distancia,positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "AND", 1, 24, (255,255,255))
            p_or = Button(positon_bootoms[0],positon_bootoms[1]+5*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "OR", 1, 24, (255,255,255))
            p_xor = Button(positon_bootoms[0],positon_bootoms[1]+6*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "XOR", 1, 24, (255,255,255))

            p_nand= Button(positon_bootoms[0],positon_bootoms[1]+7*distancia,positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "NAND", 1, 24, (255,255,255))
            p_nor = Button(positon_bootoms[0],positon_bootoms[1]+8*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "NOR", 1, 24, (255,255,255))
            p_xnor = Button(positon_bootoms[0],positon_bootoms[1]+9*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "XNOR", 1, 24, (255,255,255))

            p_not= Button(positon_bootoms[0],positon_bootoms[1]+10*distancia,positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "NOT", 1, 24, (255,255,255))
            p_pin = Button(positon_bootoms[0],positon_bootoms[1]+11*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "PIN", 1, 24, (255,255,255))
            p_out = Button(positon_bootoms[0],positon_bootoms[1]+12*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "POUT", 1, 24, (255,255,255))
            P_Buttons = [p_and,p_or,p_xor,p_nand,p_nor,p_xnor,p_not,p_pin,p_out]

            #botones (100,100,100) caja (255,255,255) texto dentro de la caja
            a_clablear= Button(positon_bootoms[0],positon_bootoms[1]+4*distancia,positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "Cablear", 1, 24, (255,255,255))
            a_borrar = Button(positon_bootoms[0],positon_bootoms[1]+5*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Borrar", 1, 24, (255,255,255))
            A_Buttons = [a_clablear,a_borrar]

            a_clablear= Button(positon_bootoms[0],positon_bootoms[1]+4*distancia,positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "Unir", 1, 24, (255,255,255))
            a_borrar = Button(positon_bootoms[0],positon_bootoms[1]+5*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Borrar", 1, 24, (255,255,255))
            a_cancelar = Button(positon_bootoms[0],positon_bootoms[1]+6*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Cancelar", 1, 24, (255,255,255))
            Cableando_Buttons = [a_clablear,a_borrar,a_cancelar]

            a_clablear= Button(positon_bootoms[0],positon_bootoms[1]+4*distancia,positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "Cablear", 1, 24, (255,255,255))
            a_borrar = Button(positon_bootoms[0],positon_bootoms[1]+5*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Borrar", 1, 24, (255,255,255))
            a_cancelar = Button(positon_bootoms[0],positon_bootoms[1]+6*distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Cancelar", 1, 24, (255,255,255))
            Borrando_Buttons = [a_clablear,a_borrar,a_cancelar]
            
            #Botones que intercambian entre colores y colores predeterminados
            P_number1 = Button(sw-50, positon_bootoms[1]+3*distancia, 15,15, (80,80,80), "")
            P_number1.clicked = True
            P_number2 = Button(sw-30, positon_bootoms[1]+3*distancia, 15,15, (80,80,80), "")
            C_Buttons = [P_number1, P_number2]

            e_Pausar= Button(positon_bootoms[0],positon_bootoms[1],positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "Pausar", 1, 24, (255,255,255))
            e_tabla = Button(positon_bootoms[0],positon_bootoms[1]+distancia,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Tabla", 1, 24, (255,255,255))
            ejec_Buttons = [e_Pausar,e_tabla]
        
        #pinta el el aria de trabajo
        self.workspace.Draw(self.screen)
        #pinta las paredes
        self.draw_walls()
        #pinta los botones
        #para el cableado y y selección
        #i = 0
        self.AlgoSeleccionado = False
        self.Cablear = False
        self.In = None
        self.Out = None
        self.ejecutando_tabla=False
        self.ejecutamos_2=False

        while not listo: #comienzo a capturar los elementos
            if not (self.Ejecutar):
                for but in SL_Buttons:
                    but.Draw(self.screen)
                if selected ==0:
                    for but in P_Buttons:
                        but.Draw(self.screen)
                    self.Cablear=False
                    self.Borrar=False
                elif selected ==1:
                    #print(self.ca)
                    if self.Cablear:
                        for but in Cableando_Buttons:
                            but.Draw(self.screen)
                    elif self.Borrar:
                        for but in Borrando_Buttons:
                            but.Draw(self.screen)
                    else:
                        for but in A_Buttons:
                            but.Draw(self.screen)
                for but in C_Buttons:
                    but.Draw(self.screen)
            else:
                for but in ejec_Buttons:
                    but.Draw(self.screen)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #permite salir con ESC
                        listo=True
                        sys.exit()
                if not(self.Ejecutar) :
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #print(event.button)
                        #si esta en el grid (Lienzo)
                        if pygame.mouse.get_pos()[0] < self.workspace.xCount*self.workspace.cellSize and pygame.mouse.get_pos()[1] < self.workspace.yCount*self.workspace.cellSize:
                            print("ESTAS EN WORKSPACE")
                            # obtiene la posicion el evento es decir del CLICK
                            x, y = event.pos       
                            for Componente in self.Componentes.values():
                                #print(self.AlgoSeleccionado)
                                if Componente.rect.collidepoint(x, y):
                                    
                                    if self.Cablear:

                                        if not self.In:
                                            print("Seleccionado el primer componente: " + str(Componente))
                                            self.In = Componente
                                            
                                        elif not self.Out:
                                            print("Seleccionado el segundo componente: " + str(Componente))
                                            self.Out = Componente
                                        
                                    elif self.AlgoSeleccionado==False:
                                        print('Objeto seleccionado')
                                        Componente.seleccionar()
                                        self.AlgoSeleccionado = Componente
                                    elif self.AlgoSeleccionado!=False:
                                        print('Objeto soltar')
                                        Componente.seleccionar()
                                        self.AlgoSeleccionado = False
                                #else:
                                    #por si no ccolisiona con el objeto
                                    #if self.AlgoSeleccionado!=False:
                                        #if self.AlgoSeleccionado in self.Componentes.values():
                                            #self.AlgoSeleccionado.seleccionar()
                                            #self.AlgoSeleccionado = False
                            pos=(x,y)
                            if self.Borrar:
                                for Componente in self.Cables:
                                    if Componente.Colisiona(pos):
                                        if self.AlgoSeleccionado==False:
                                            print('Objeto seleccionado')
                                            self.AlgoSeleccionado = Componente

                                    

                        #sino esta en el workspacce
                        else:
                            #print("No estas en el worspace")
                            if event.button == 1:
                                for i,but in enumerate(SL_Buttons):
                                    #print("encima de un boton")
                                    #print(but.rollOver)
                                    if but.rollOver:
                                        #print(i)
                                        if i == 0:
                                            listo=True
                                            sys.exit()
                                        if i == 1:
                                            print("Ejecutando")
                                            self.Ejecutar=True
                                       
                                            
                                if selected ==0:
                                    #botones de puertas
                                    for i,but in enumerate(P_Buttons):
                                        if but.rollOver:
                                            if i == 0:
                                                print("Se pulsó la tecla A")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos)
                                                self.Borrar=False
                                                print(self.Componentes)
                                            if i == 1:
                                                print("Se pulsó la tecla OR")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos,1)
                                                self.Borrar=False
                                                print(self.Componentes)
                                            if i == 2:
                                                print("Se pulsó la tecla XOR")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos,2)
                                                self.Borrar=False
                                                print(self.Componentes)
                                            if i == 3:
                                                print("Se pulsó la tecla NAND")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos,3)
                                                self.Borrar=False
                                                print(self.Componentes)
                                            if i == 4:
                                                print("Se pulsó la tecla NOR")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos,4)
                                                self.Borrar=False
                                                print(self.Componentes)
                                            if i == 5:
                                                print("Se pulsó la tecla XNOR")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos,5)
                                                self.Borrar=False
                                                print(self.Componentes)
                                            if i == 6:
                                                print("Se pulsó la tecla NOT")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos,6)
                                                self.Borrar=False
                                                print(self.Componentes)
                                            if i == 7:
                                                print("Se pulsó la tecla PIN")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos,7)
                                                self.Borrar=False
                                                print(self.Componentes)
                                            if i == 8:
                                                print("Se pulsó la tecla POU")
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.Crear_puertas(mouse_pos,8)
                                                self.Borrar=False
                                                print(self.Componentes)


                                if selected ==1:
                                    #botones de entre acciones y puertas
                                    if self.Cablear:
                                        for i,but in enumerate(Cableando_Buttons ):
                                            if but.rollOver:
                                                if i == 0:
                                                    print("cableando")
                                                    self.Cableando()
                                                    print(self.Componentes)
                                                if i == 1:
                                                    if len(self.Componentes)!=0: 
                                                        print("Borrando")
                                                        self.cancelar()
                                                        self.Borrar=True
                                                if i == 2:
                                                    print("Cancelando")
                                                    self.cancelar()
                                    elif self.Borrar:
                                        for i,but in enumerate(Borrando_Buttons ):
                                            if but.rollOver:
                                                if i == 0:
                                                    print("cableando")
                                                    self.Borrar=False
                                                    self.Cableando()
                                                    print(self.Componentes)
                                                if i == 1:
                                                    if len(self.Componentes)!=0: 
                                                        print("Borrando")
                                                        self.Borrar=True
                                                if i == 2:
                                                    print("Cancelando")
                                                    self.cancelar()
                                    else:
                                        for i,but in enumerate(A_Buttons):
                                            if but.rollOver:
                                                if i == 0:
                                                    print("cableando")
                                                    self.Cableando()
                                                    print(self.Componentes)
                                                if i == 1:
                                                    if len(self.Componentes)!=0: 
                                                        print("Borrando")
                                                        self.Borrar=True
                                                

                                for i,but in enumerate(C_Buttons):
                                    if but.rollOver:
                                        if i != selected:
                                            selected=i
                                            but.clicked=True
                                            for subbutton in C_Buttons:
                                                if C_Buttons.index(subbutton) != selected:
                                                    subbutton.clicked = False
                                            

                        """#para los cables 
                        for componente in self.Cables.key():
                            elif self.AlgoSeleccionado == False:
                                print('Objeto seleccionado')
                                Componente.seleccionar()
                                self.AlgoSeleccionado = Componente
                            else:
                                print('Objeto soltado')
                                Componente.seleccionar()
                                self.AlgoSeleccionado = False"""
                    
                    elif (event.type == pygame.MOUSEMOTION):
                        if pygame.mouse.get_pos()[0] < self.workspace.xCount * self.workspace.cellSize and pygame.mouse.get_pos()[1] < self.workspace.yCount * self.workspace.cellSize:
                            for Componente in self.Componentes.values():
                                if Componente.seleccionado and not self.Borrar:
                                    #self.workspace.Draw(self.screen)
                                    #pinta las paredes
                                    #self.draw_walls()
                                    #pinta los botones
                                    #print("Moviendo...")
                                    Componente.mover()
        
                        else:
                            # es para el cambio de color de los botones
                            for but in SL_Buttons:
                                if but.subsurface.get_rect(topleft=but.pos).collidepoint(pygame.mouse.get_pos()):
                                    but.rollOver = True
                                else:
                                    but.rollOver = False
                            
                            for but in P_Buttons:
                                if but.subsurface.get_rect(topleft=but.pos).collidepoint(pygame.mouse.get_pos()):
                                    but.rollOver = True
                                else:
                                    but.rollOver = False

                            if selected ==1:
                                #print(self.ca)
                                if self.Cablear:
                                    for but in Cableando_Buttons:
                                        if but.subsurface.get_rect(topleft=but.pos).collidepoint(pygame.mouse.get_pos()):
                                            but.rollOver = True
                                        else:
                                            but.rollOver = False
                                elif self.Borrar:
                                    for but in Borrando_Buttons:
                                        if but.subsurface.get_rect(topleft=but.pos).collidepoint(pygame.mouse.get_pos()):
                                            but.rollOver = True
                                        else:
                                            but.rollOver = False
                                else:
                                    for but in A_Buttons:
                                        if but.subsurface.get_rect(topleft=but.pos).collidepoint(pygame.mouse.get_pos()):
                                            but.rollOver = True
                                        else:
                                            but.rollOver = False
                            
                            for but in C_Buttons:
                                if but.subsurface.get_rect(topleft=but.pos).collidepoint(pygame.mouse.get_pos()):
                                    but.rollOver = True
                                else:
                                    but.rollOver = False
        
                    elif event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_a:
                            print("Se pulsó la tecla A")
                            self.Crear_puertas(pygame.mouse.get_pos())
                        
                        if event.key == pygame.K_c:
                            if not self.Cablear:
                                print("Comienza el cableado")
                                self.Cablear = True
                                selected=1
                            else:
                                print("Se detuvo el cableado")
                                self.Cablear = False
                                self.In = None
                                self.Out = None
                                
                        
                        if event.key == pygame.K_j and self.Cablear:
                            self.Cableando()
                                
                        
                        if event.key == pygame.K_SPACE:
                            print("Borrar Cables")
                            for wire in Cables:
                                wire.borrar_conexiones()
                    
                    #elif event.type == pygame.VIDEORESIZE:
                    #print(event)
                    #self.Maximizar=self.screensize.copy()
                    #SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                    #self.screensize = [SCREEN_WIDTH, SCREEN_HEIGHT]
                    #print(self.Maximizar)
                    #print(self.screensize)
                    #self.cambiar_tamaño()
                    #self.workspace.Draw(self.screen)
                    #self.draw_walls()"""
                else:
                    #si esta en ejecución
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pos()[0] < self.workspace.xCount*self.workspace.cellSize and pygame.mouse.get_pos()[1] < self.workspace.yCount*self.workspace.cellSize:
                            print("ESTAS EN EL WORKSPACE")
                            # obtiene la posicion del CLICK
                            x, y = event.pos       
                            for Componente in self.Pines.values():
                                #cambia el estado de del pin de entrada
                                print(self.AlgoSeleccionado)
                                if Componente.rect.collidepoint(x, y):
                                        Componente.Salida= not(Componente.Salida)
                                        Componente.cambio()
                                        if self.ejecutando_tabla ==True:
                                            self.ejecutamos_2=True

                        
                        elif event.button == 1:
                                for i,but in enumerate(ejec_Buttons):
                                    #print("Funciono")
                                    #print(but.rollOver)
                                    if but.rollOver:
                                        if i == 0:
                                            self.reset()
                                            self.Ejecutar=False
                                        elif i==1:
                                            if self.ejecutando_tabla==False:
                                                self.tabla()
                                                self.ejecutando_tabla=True
                                            else:
                                                self.ejecutando_tabla=False
                                                self.screen=pygame.display.set_mode(self.screensize,pygame.RESIZABLE)
                                                #self.screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                                
                                 
                    elif (event.type == pygame.MOUSEMOTION):
                        # para saber si el raton esta pasando por enciama de los botones
                        for but in ejec_Buttons:
                            if but.subsurface.get_rect(topleft=but.pos).collidepoint(pygame.mouse.get_pos()):
                                but.rollOver = True
                            else:
                                but.rollOver = False
            

            if self.Ejecutar:
                #print(".")
                #ejecuta la logica
                self.ejecutar_logica()
                if self.ejecutamos_2==True:
                    self.tabla()
                    self.ejecutamos_2=False

            if self.Borrar and self.AlgoSeleccionado!=False:
                #print("HOLA MATEO",self.AlgoSeleccionado)
                self.elemento_borrado=self.AlgoSeleccionado
                #print(self.elemento_borrado)
                self.Borrando(self.AlgoSeleccionado)
                self.Borrar=False
                self.AlgoSeleccionado=False
                #print(self.elemento_borrado)
            #No se
            
            self.screen.fill((255,255, 255))
            #print(self.Ejecutar)
            if self.Ejecutar:
                #print("Ejecutando")
                #print(self.workspace.color)
                self.workspace.change_color_all((0,200,200))
                #print(self.workspace.color)
            else:

                self.workspace.change_color_all((255,255,255))
                

            self.workspace.Draw(self.screen)
            self.draw_walls()
            if  self.Ejecutar:
                self.screen.blit(colorTitleFont.render("Ejecutando", True, (50,50,50)), (positon_bootoms[0]+10,positon_bootoms[1]-distancia/2))
            else:
                self.screen.blit(colorTitleFont.render("MENU", True, (50,50,50)), (positon_bootoms[0]+20,positon_bootoms[1]-distancia/2))
                if selected ==0:
                    self.screen.blit(colorTitleFont.render("Puertas", True, (50,50,50)), (positon_bootoms[0]-20,positon_bootoms[1]+3*distancia))
                elif selected ==1:
                    
                    if self.Cablear:
                        self.screen.blit(colorTitleFont.render("Cableando", True, (50,50,50)), (positon_bootoms[0]-20,positon_bootoms[1]+3*distancia))
                    elif self.Borrar:
                        self.screen.blit(colorTitleFont.render("Borrando", True, (50,50,50)), (positon_bootoms[0]-20,positon_bootoms[1]+3*distancia))
                    else:
                        self.screen.blit(colorTitleFont.render("Acciones", True, (50,50,50)), (positon_bootoms[0]-20,positon_bootoms[1]+3*distancia))
            
        

            if not(self.AlgoSeleccionado):
                self.texto=None
            else:
                self.texto=self.AlgoSeleccionado
            if self.Cablear:
                self.screen.blit(fileFont.render("Elemento 1 ", True, (50,50,50)), (sw-320,sh-90))
                self.screen.blit(fileFont.render(str(self.In), True, (0, 0, 0)), (sw-320,sh-70))
                self.screen.blit(fileFont.render("Elemento 2 ", True, (50,50,50)), (sw-320,sh-50))
                self.screen.blit(fileFont.render(str(self.Out), True, (0, 0, 0)), (sw-320,sh-30))

            elif self.elemento_borrado:
                self.screen.blit(fileFont.render("Elemento Borrado", True, (50,50,50)), (sw-320,sh-50))
                self.screen.blit(fileFont.render(str(self.elemento_borrado), True, (0, 0, 0)), (sw-320,sh-30))
                
            else:    
                self.screen.blit(fileFont.render("Objeto Selecionado", True, (50,50,50)), (sw-320,sh-50))
                self.screen.blit(fileFont.render(str(self.texto), True, (0, 0, 0)), (sw-320,sh-30))
            self.screen.blit(self.logo, (positon_bootoms[0]-20,sh-55))
            for Componente in self.Componentes.values():
                Componente.mostrar(self.screen)
            for Componente,puertas in self.Cables.items():
                Componente.graficar(puertas[0],puertas[1],self.screen)

            if self.AlgoSeleccionado:
                self.elemento_borrado=None
            
            #print(self.Componentes)

        pygame.display.quit()
        pygame.quit()

    def draw_walls(self):
        wall_color = (50,50,50)
        #Grosor de las paredes
        wall_thickness = 4
        sw,sh=self.screensize
        #tamaño=self.workspace.xCount * self.workspace.cellSize
        #if tamaño>200:
        #tamaño=200
        #print(sw)
        #print(self.workspace.xCount * self.workspace.cellSize)
        tamano=sw-160
        #print(tamaño)
        #(150,0,150) lado derecho de la pantalla herramientas
        pygame.draw.rect(self.screen, (150,150,150), (tamano, 0, sw,self.workspace.yCount*self.workspace.cellSize))
        #(80,80,80) lado abajo botones
        #pygame.draw.rect(self.screen, (80,80,80), (0, self.workspace.xCount * self.workspace.cellSize, sw, self.workspace.yCount*self.workspace.cellSize))
        #entre el workspace y la barrade herramientas a ala derecha
        
        #print(self.workspace.yCount*self.workspace.cellSize)
        pygame.draw.rect(self.screen, wall_color, (tamano, 0, wall_thickness,self.workspace.yCount*self.workspace.cellSize))
        #pygame.draw.rect(self.screen, wall_color, (0, self.workspace.yCount*self.workspace.cellSize-wall_thickness, sw, wall_thickness))

        #cuadrado que va por fuera
        #arriba de todo parez
        pygame.draw.rect(self.screen, wall_color, (0, 0, sw, wall_thickness))
        #lateral derecho 
        pygame.draw.rect(self.screen, wall_color, (sw-wall_thickness, 0, wall_thickness, sh))
        #lateral izquierdo
        pygame.draw.rect(self.screen, wall_color, (0, 0, wall_thickness, sh))
        #abajo todo
        pygame.draw.rect(self.screen, wall_color, (0, sh - wall_thickness, sw, wall_thickness))

    def cambiar_tamaño(self):
        self.workspace=Grid(int(64*self.screensize[0]/850),int(68*self.screensize[1]/950),12, 0, 0, [255, 255, 255])
        self.draw_walls()

    def Crear_puertas(self,pos,num=0,):
        if num==0:
            self.Componentes[len(self.Componentes)] = PuertaAND(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)
        if num==1:
            self.Componentes[len(self.Componentes)] = PuertaOR(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)
        if num==2:
            self.Componentes[len(self.Componentes)] = PuertaXOR(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)
        if num==3:
            self.Componentes[len(self.Componentes)] = PuertaNAND(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)
        if num==4:
            self.Componentes[len(self.Componentes)] = PuertaNOR(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)
        if num==5:
            self.Componentes[len(self.Componentes)] = PuertaXNOR(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)
        if num==6:
            self.Componentes[len(self.Componentes)] = PuertaNOT(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            self.Una_solo_entrada[len(self.Una_solo_entrada)]=self.Componentes[len(self.Componentes)-1]
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)
        if num==7:
            self.Componentes[len(self.Componentes)] = PinIN(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            self.Pines[len(self.Pines)] = self.Componentes[len(self.Componentes)-1]
            
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)
        if num==8:
            self.Componentes[len(self.Componentes)] = PinOUT(pos[0]-100,pos[1]-80)
            self.Todos[len(self.Todos)] = self.Componentes[len(self.Componentes)-1]
            self.Una_solo_entrada[len(self.Una_solo_entrada)]=self.Componentes[len(self.Componentes)-1]
            #Para que al crearlo se mueva directamente
            self.Componentes[len(self.Componentes)-1].seleccionar()
            self.AlgoSeleccionado = self.Componentes[len(self.Componentes)-1]
            #print(self.AlgoSeleccionado)
            #print(self.Todos)

    def Cableando(self):
        if not self.Borrar:
            if not self.Cablear:
                print("Comienza el cableado")
                self.Cablear = True
            #Mira si hay dos componentes
            elif self.In and self.Out:
                #mira si son diferentes
                if self.In != self.Out:
                    print(self.Out,self.Una_solo_entrada.values())
                    print(self.Out in self.Una_solo_entrada.values())
                    #comprueba que la entrada no este llena
                    if self.Out in self.Una_solo_entrada.values():
                        if not(self.Out.lleno):
                            print("un solo componente")
                            placeholder = Cable(len(self.Cables))
                            self.Cables[placeholder]=[self.In,self.Out]
                            placeholder.conectar(self.In,self.Out)
                            placeholder.graficar(self.In,self.Out,self.screen)
                            self.Out.lleno=not(self.Out.lleno)
                            self.Todos[len(self.Todos)] = placeholder
                            self.In = None
                            self.Out = None
                            self.Cablear = False
                        else:
                            self.Out = None
                    elif self.Out in self.Pines.values():
                        self.Out = None
                    else:
                        print("Unidos")
                        placeholder = Cable(len(self.Cables))
                        self.Cables[placeholder]=[self.In,self.Out]
                        placeholder.conectar(self.In,self.Out)
                        placeholder.graficar(self.In,self.Out,self.screen)
                        self.Todos[len(self.Todos)] = placeholder
                        self.In = None
                        self.Out = None
                        self.Cablear = False
                else:
                    self.Out=None
                               
    def cancelar(self):
        #cancela la accion
        if self.Cablear:
            print("Se detuvo el cableado")
            self.Cablear = False
            self.In = None
            self.Out = None
        if self.Borrar:
            print("Se detuvo el Borrado")
            self.Borrar=False
            self.AlgoSeleccionado=False

    def Borrando(self,componente):
        #print('borrar')
        #key_borrar=self.get_keys_with_value(self.Todos,componente)
        #print(componente)
        print(self.Componentes)
        if componente in self.Componentes.values():
            key_componente_borrar=self.get_keys_with_value(self.Componentes,componente)
            print(self.Cables)
            print(self.Componentes)
            #print(self.Todos)
            print("Entrada",componente.Entradas)
            print("Salida",componente.Salida)
            print("Borramos una puerta")

            #print(componente.Entradas)
            lista_borrar=componente.Entradas.copy()
            for i in lista_borrar.keys():
                #print(i)
                #print(self.Cables)
                i.borrar_conexiones()
                self.Cables.pop(i)
            lista_borrar=componente.Siguiente.copy()
            for i in lista_borrar.keys():
                #print(i)
                #print(self.Cables)
                i.borrar_conexiones()
                self.Cables.pop(i)
                
            print("Entrada",componente.Entradas)
            print("Salida",componente.Salida)
            #print(key_componente_borrar)
            #print(key_borrar)
            self.Componentes.pop(key_componente_borrar[0])
            lista=self.Componentes.copy()
            self.Componentes={}
            for value in lista.values():
                self.Componentes[len(self.Componentes)]=value
            #self.Todos.pop(key_borrar[0])
            print(self.Cables)
            print(self.Componentes)
            #print(self.Todos)
            if componente in self.Pines.values():
                key_componente_borrar=self.get_keys_with_value(self.Pines,componente)
                self.Pines.pop(key_componente_borrar[0])
                lista=self.Pines.copy()
                self.Pines={}
                for value in lista.values():
                    self.Pines[len(self.Pines)]=value

        elif componente in self.Cables:
            elementos=self.Cables[componente]
            for elemento in elementos:
                print(elemento)
            
                if elemento in self.Una_solo_entrada.values():
                    elemento.lleno=False
            print(componente)
            print(self.Cables)
            print("Borramos un cable")
            componente.borrar_conexiones()
            self.Cables.pop(componente)

    def get_keys_with_value(self,dic, value):
        #obtenos las claves de de un valor
        return [key for key, val in dic.items() if val == value]

    def ejecutar_logica(self):
        self.ya_ejecutado=[]
        encontrado=False
        for Component in self.Componentes.values():
            #funciona para 1
            #if len(Component.Siguiente)==0:
                #Component.logica()
                #print(Component)
            #if len(Component.Entradas)==0 and not(encontrado):
                #encontrado=True
                #Component.logica()
                #self.ya_ejecutado.append(Component)
                #for i in Component.Siguiente:
                    #Component.logica()
                    #self.ya_ejecutado.append(Component)
            if len(Component.Entradas)!=0 :
                Component.logica()

    def reset(self):
        for componente in self.Componentes.values():
            print(componente.Salida)
            componente.Salida=False
            print(componente.Salida)
        for component in self.Componentes.values():
            if len(component.Entradas)!=0 :
                component.logica()
            #print(component,self.Pines.values())
            if component in self.Pines.values():
                component.cambio()

    def tabla(self):
            
            self.screen=pygame.display.set_mode(self.screensize,pygame.RESIZABLE)
            self.workspace.Draw(self.screen)
            self.draw_walls()
            for Componente in self.Componentes.values():
                Componente.mostrar(self.screen)
            for Componente,puertas in self.Cables.items():
                Componente.graficar(puertas[0],puertas[1],self.screen)
    
            pygame.display.flip()
            root = Tk()
            w = 700 # ancho de la  Tk root
            h = 600# altura de la Tk root

            # obtiene el alto y haco de la pantalla
            ws = root.winfo_screenwidth() 
            hs = root.winfo_screenheight() 

            # calcula las coordenadas para la ventana en función de la pantalal
            #x = (ws/2) 
            x = (ws*7/14)
            y = (hs/2) - (h/2)

            # mandamos las dimensiones de la pantalla
            # y el lugar
            root.geometry('%dx%d+%d+%d' % (w, h, x, y))
            root.call('wm', 'attributes', '.', '-topmost', '1')
            App(root,self.Componentes)
            root.mainloop()
            #self.screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    
s=LogAJD()
s.graficar()
