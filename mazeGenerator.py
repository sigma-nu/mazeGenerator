import sys
import pygame
import random

# Recursive maze generation!
#
# This algorithm uses a randomized depth-first search with back-tracking to visit random cells and add them to the
# maze. This will also be my first time using the stack data structure! Exciting stuff!
#
# To do this I will be following the psuedo-code:
# 1. Make the initial cell the current cell and mark it as visited.
# 2. While there are unvisited cells:
#    1. If the current cell has any unvisited neighbours:
#       1. Choose randomly one of the unvisited neighbours.
#       2. Push the current cell to the stack.
#       3. Remove the wall between the current cell and the chosen cell.
#       4. Make the chosen cell the current cell and mark it as visited.
#    2. Else if the stack is not empty:
#       1. Pop a cell from the stack.
#       2. Make it the current cell.
#
# When displayed:
# - Blue is a completed cell
# - Red is the current cell
# - Light red is a cell still in the stack
# - Light blue is an unvisited cell

# Frame rate
FPS = 30
clock = pygame.time.Clock()

# Window size
size = width, height = 600, 600
rows = 20
cols = 20

# Border and cell dimesions
b_w = int(width/20)
b_h = int(height/20)
c_w = (width-2*b_w)/cols
c_h = (height-2*b_h)/rows

# Initialize screen
screen = pygame.display.set_mode(size)

# Colours
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
purple = 50, 0, 100
l_grey = 220, 220, 220

l_blue = 157, 195, 230
l_l_blue = 223, 235, 247
l_red = 255, 175, 175

# Main code -----
class Cell():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True] # Top, Left, Bottom, Right
        self.visited = False
        self.inStack = False

    def pickNeighbour(self):
        i = self.i
        j = self.j
        neighbours = []
        if j-1 >= 0 and not maze[j-1][i].visited: # Top
            neighbours.append(maze[j-1][i])
        if i-1 >= 0 and not maze[j][i-1].visited: # Left
            neighbours.append(maze[j][i-1])
        if j+1 < cols and not maze[j+1][i].visited: # Bottom
            neighbours.append(maze[j+1][i])
        if i+1 < rows and not maze[j][i+1].visited: # Right
            neighbours.append(maze[j][i+1])

        if len(neighbours) > 0:
            rand = random.randint(0, len(neighbours)-1)
            return neighbours[rand]
        return 0

    def draw(self):
        x = self.i * c_w + b_w
        y = self.j * c_h + b_h
        colour = l_l_blue
        if self.visited:
            colour = l_blue
        if self.inStack:
            colour = l_red
        pygame.draw.rect(screen, colour, (x, y, c_w, c_h))
        colour = black
        if self.walls[0]: # Top
            pygame.draw.line(screen, colour, (x, y), (x + c_w, y), 2)
        if self.walls[1]: # Left
            pygame.draw.line(screen, colour, (x, y), (x, y + c_h), 2)
        if self.walls[2]: # Bottom
            pygame.draw.line(screen, colour, (x, y + c_h), (x + c_w, y + c_h), 2)
        if self.walls[3]: # Right
            pygame.draw.line(screen, colour, (x + c_w, y), (x + c_w, y + c_h), 2)
    
    def highlight(self):
        x = self.i * c_w + b_w
        y = self.j * c_h + b_h
        pygame.draw.rect(screen, red, (x+5, y+5, c_w-8, c_h-8))



def removeWall(cell, neighbour):
    difi = cell.i - neighbour.i
    difj = cell.j - neighbour.j
    if difj == 1: # Top
        cell.walls[0] = False
        neighbour.walls[2] = False
    if difi == 1: # Left
        cell.walls[1] = False
        neighbour.walls[3] = False
    if difj == -1: # Bottom
        cell.walls[2] = False
        neighbour.walls[0] = False
    if difi == -1: # Right
        cell.walls[3] = False
        neighbour.walls[1] = False

def drawMaze():
    for i in range(cols):
        for j in range(rows):
            maze[j][i].draw()


maze = [[Cell(i, j) for i in range(cols)] for j in range(rows)]
stack = []

current = maze[0][0]
current.visited = True

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(l_grey)
    drawMaze()
    current.highlight()

    neighbour = current.pickNeighbour()
    if neighbour != 0:
        current.inStack = True
        stack.append(current)
        removeWall(current, neighbour)
        neighbour.visited = True
        current = neighbour
    elif len(stack) > 0:
        current.inStack = False
        current = stack.pop()
    else:
        current.inStack = False

    pygame.display.flip()