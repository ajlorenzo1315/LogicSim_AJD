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
   from pygame.locals import *
   import  os
except:
   import install_requirements
   import pygame 
   from tkinter import *
   from tkinter import messagebox
   from pygame.locals import *
   from tkinter.filedialog import askopenfilename, asksaveasfilename
   import os
import sys

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

def SaveFile(gridObject, filePath):
    global fileName

    if filePath:
        if len(filePath) >= 4:  # This just makes sure we have .txt at the end of our file selection
            if filePath[-4:] != '.txt':
                filePath = filePath + '.txt'
        else:
            filePath = filePath + '.txt'

        file = open(filePath, "w")

        for row in range(len(gridObject.grid)):
            for pixel in gridObject.grid[row]:
                colorVal = str(pixel.color[0]) + "," + str(pixel.color[1]) + "," + str(pixel.color[2])
                file.write(colorVal + "\n")

        file.close()

        filePathList = filePath.split("/")
        fileName = filePathList[-1]
        pygame.display.set_caption("Pyint by Burak - " + fileName)

def draw_walls(screen):
    wall_color = (50,50,50)
    #Grosor de las paredes
    wall_thickness = 4
    sw,sh=screensize
    #(150,0,150) lado derecho de la pantalla herramientas
    pygame.draw.rect(screen, (150,150,150), (workspace.xCount * workspace.cellSize, 0, sw, workspace.yCount*workspace.cellSize))
    #(80,80,80) lado abajo botones
    #pygame.draw.rect(screen, (80,80,80), (0, workspace.xCount * workspace.cellSize, sw, workspace.yCount*workspace.cellSize))
    #entre el workspace y la barrade herramientas a ala derecha
    pygame.draw.rect(screen, wall_color, (workspace.xCount * workspace.cellSize, 0, wall_thickness, workspace.yCount*workspace.cellSize))
    #pygame.draw.rect(screen, wall_color, (0, workspace.yCount*workspace.cellSize-wall_thickness, sw, wall_thickness))

    #cuadrado que va por fuera
    #arriba de todo parez
    pygame.draw.rect(screen, wall_color, (0, 0, sw, wall_thickness))
    #lateral derecho 
    pygame.draw.rect(screen, wall_color, (sw-wall_thickness, 0, wall_thickness, sh))
    #lateral izquierdo
    pygame.draw.rect(screen, wall_color, (0, 0, wall_thickness, sh))
    #abajo todo
    pygame.draw.rect(screen, wall_color, (0, sh - wall_thickness, sw, wall_thickness))

pygame.init()
W = 700
H = 600
sys.setrecursionlimit(1000)
screensize = [W, H]
y_origen = 100
delta_y = 100
#desplazamiento a mayores si lo queremos
offset = [0, 0]
separacion = 6 #numero mas alto es menos separacion


scrolling = False
sw,sh=screensize
#screen = pygame.display.set_mode(screensize, pygame.RESIZABLE) #de esta manera la pantalla puede agrandarse o encojerse
screen=pygame.display.set_mode(screensize)
screen.fill((255,255, 255))
workspace = Grid(int(64*sh/850),int(64*sw/950),12, 0, 0, [255, 255, 255])
workspace.Draw(screen)
draw_walls(screen)
listo = False
positon_bootoms=[sw-130,20,int(160*sh/850),int(40*sw/950)]
#botones (100,100,100) caja (255,255,255) texto dentro de la caja
save_b = Button(positon_bootoms[0],positon_bootoms[1],positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "Save", 1, 24, (255,255,255))
load_b = Button(positon_bootoms[0],positon_bootoms[1]+40,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Load", 1, 24, (255,255,255))
export_b = Button(positon_bootoms[0],positon_bootoms[1]+80,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "Export", 1, 24, (255,255,255))
SL_Buttons = [save_b, load_b, export_b]

#botones (100,100,100) caja (255,255,255) texto dentro de la caja
p_and= Button(positon_bootoms[0],positon_bootoms[1]+140,positon_bootoms[2],positon_bootoms[3], (100, 100, 100), "AND", 1, 24, (255,255,255))
p_or = Button(positon_bootoms[0],positon_bootoms[1]+180,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "OR", 1, 24, (255,255,255))
p_xor = Button(positon_bootoms[0],positon_bootoms[1]+220,positon_bootoms[2],positon_bootoms[3],(100, 100, 100), "XOR", 1, 24, (255,255,255))
P_Buttons = [p_and,p_or,p_xor]
for but in SL_Buttons:
    but.Draw(screen)
for but in P_Buttons:
    but.Draw(screen)
while not listo: #comienzo a capturar los elementos 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #permite salir con ESC
            listo=True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i,but in enumerate(SL_Buttons):
                    if but.rollOver:
                        if i == 0:
                            cPath = FileManager(1)
                            SaveFile(workspace, cPath)
                        elif i == 1:
                            cPath = FileManager(0)
                            OpenFile(cPath)
                        elif i == 2:
                            cPath = FileManager(2)
                            if cPath:
                                Capture(screen, cPath + ".png", (4,4), (764,760))
                                fileName = cPath.split("/")[-1] + ".png"
           
pygame.display.quit()
pygame.quit()

