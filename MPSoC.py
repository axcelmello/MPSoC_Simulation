import math
import json
import random
import copy
from TaskSctruct import Task

global_matrix = []
nlines = 0
ncolumns = 0
qtTasks = 0

class MPSoC:
    def __init__(self, qtNodos, qtTask):
        self.qtNodos = qtNodos
        self.qtTask = qtTask

        global global_matrix
        global_matrix = self.buildMatriz(qtNodos, qtTask)
        self.matrix = global_matrix

        self.nline = 0
        self.ncolumn = 0

        #Note: matrix[x][y] where x = line and y = column

    def getNline(self):
        return int(self.nline)
    def getNcolumn(self):
        return int(self.ncolumn)

    def buildMatriz(self, quant, qtTask):
        nline = math.ceil(math.sqrt(quant))
        ncolumn = math.ceil(quant / nline)

        self.nline = nline
        self.ncolumn = ncolumn

        matrix, line = [], []
        qtTask = qtTask

        #pass the global variables that will be used later
        global nlines
        nlines = nline
        global ncolumns
        ncolumns = ncolumn
        global qtTasks
        qtTasks = qtTask


        for i in range(nline):
            line = []
            for j in range(ncolumn):
                line.append(NodoChaveamento(i, j, qtTask))
            matrix.append(line)

        matrix[0][0] = NodoControle()

        return matrix

    def showMatrixUsage(self):
        global global_matrix
        print()
        print("Load transfered in each Node:")
        for line in range(len(global_matrix)):
            print()
            for column in range(len(global_matrix[0])):
                print(global_matrix[line][column].count, end= " ")
        print()

class NodoControle():

    def __init__(self):
        t1 = Task("A", [1,2], [0, 1], 1)
        t2 = Task("B", [1,2], [2, 0], 1)
        t3 = Task("C", [1,2], [2, 0], 1)

        self.tasks = "C" #alias to print funcions
        self.count = "C" #alias to print funcions

        self.data = ""
        self.progs = {
            "progA" : [t1, t1, t1, t1, t1, t1, t1],
            "progB" : [t2, t2, t2]
        }

    def __str__(self):
        return "Nodo de Controle"

    def readJson(self, localFile):
        self.data = json.load(open(localFile))

    def startProcess(self):

        for key in self.progs:
            global global_matrix
            nline = len(global_matrix)
            ncolumn = len(global_matrix[0])

            print("Allocating ", key, "program.")

            for tasks in self.progs.get(key):
                x = random.randint(0, nline - 1) #size nline
                y = random.randint(0, ncolumn - 1) #size ncolumn
                if x == 0 and y == 0:
                    x = 1
                self.flood_fill(x, y, key)

            if len(self.progs.get(key)) > 0:
                #print("Double checked!")
                for tasks in self.progs.get(key):
                    x = random.randint(0, nline - 1)  # size nline
                    y = random.randint(0, ncolumn - 1)  # size ncolumn
                    if x == 0 and y == 0:
                        x = 1
                    self.flood_fill(x, y, key)

        print("Programs Allocated!")

    def executeTasks(self):
        print("Starting execution.")
        global global_matrix
        for line in range(len(global_matrix)):
            for column in range(len(global_matrix[0])):
                #Ignore the ControlNode
                if line != 0 or column != 0:
                    for task in global_matrix[line][column].tasks:
                        global_matrix[line][column].sendLoad(task)
                    #Clean the Tasks in the node
                    global_matrix[line][column].tasks = []


######## Flood Recursive functions
    def is_valid_point(self, nline, ncolumn):
        global nlines
        global ncolumns

        if nline == 0 and ncolumn == 0:
            return False

        return nline >= 0 and nline < nlines\
               and ncolumn >= 0 and ncolumn < ncolumns

    def is_full(self, line, column):
        global global_matrix
        global qtTasks
        #print(len(global_matrix[line][column].tasks))
        #print(qtTasks)
        if len(global_matrix[line][column].tasks) == qtTasks:
            return True

    def have_task(self, key):
        if len(self.progs.get(key)) > 0:
            return True
        else:
            return False

    def allocateTask(self, key, l, c):
        #print(self.progs.get(key)[0])
        self.progs.get(key)[0].origin[0] = l
        self.progs.get(key)[0].origin[1] = c
        #print("ALLOCATING", self.progs.get(key)[0])
        global global_matrix
        global_matrix[0][1].recieveLoad(self.progs.get(key)[0])
        #print(key)
        #print(self.progs.get(key))
        self.progs.get(key).pop(0)
        #print("TASKS IN", key, "->", len(self.progs.get(key)))

    def get_neighbors(self, line, column):
        neighbors = []
        if self.is_valid_point(line - 1, column):
            neighbors.append((line - 1, column))
        if self.is_valid_point(line + 1, column):
            neighbors.append((line + 1, column))
        if self.is_valid_point(line, column - 1):
            neighbors.append((line, column - 1))
        if self.is_valid_point(line, column + 1):
            neighbors.append((line, column + 1))

        #print("vizinho", neighbors)
        return neighbors

    def flood_fill(self, line, column, key):

        #print(line, column, key, "flooding")

        if not self.have_task(key):
            return

        if self.is_full(line, column):
            #print(line, column, key, "FULLLL!")
            return

        self.allocateTask(key, line, column)

        neighbors = self.get_neighbors(line, column)

        for neighbor in neighbors:
            self.flood_fill(neighbor[0], neighbor[1], key)

class NodoChaveamento():
    def __init__(self, x, y, qtTask):
        self.x = x
        self.y = y
        self.tasks = []
        self.qtTask = qtTask
        self.count = 0

    def __str__(self):
        return str(self.x) + "," + str(self.y)


    def recieveLoad(self, task):
        #print("in ", self.x,self.y, task)
        global global_matrix
        if [self.x, self.y] == task.origin:
            self.tasks.append(copy.copy(task))
        else:
            if task.origin[0] > self.x:
                global_matrix[self.x + 1][self.y].recieveLoad(task)
            if task.origin[0] == self.x and task.origin[1] > self.y:
                global_matrix[self.x][self.y + 1].recieveLoad(task)
            if task.origin[0] == self.x and task.origin[1] < self.y:
                global_matrix[self.x][self.y - 1].recieveLoad(task)

    def sendLoad(self, task):
        global global_matrix
        #Register the usage of Node
        self.count = self.count + task.load

        if [self.x, self.y] == task.destiny:
            print(task, "Task executed!")
        else:
            #find x axis
            if task.destiny[0] > self.x:
                global_matrix[self.x + 1][self.y].sendLoad(task)
            if task.destiny[0] < self.x:
                #way around the ControlNode
                if self.y == 0 and self.x - 1 == 0:
                    global_matrix[self.x][self.y + 1].sendLoad(task)
                else:
                    global_matrix[self.x - 1][self.y].sendLoad(task)
           #find y axis
            if task.destiny[0] == self.x and task.destiny[1] > self.y:
                global_matrix[self.x][self.y + 1].sendLoad(task)
            if task.destiny[0] == self.x and task.destiny[1] < self.y:
                global_matrix[self.x][self.y - 1].sendLoad(task)
