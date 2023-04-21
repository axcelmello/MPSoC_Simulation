import math
import json
import random
from TaskSctruct import Task

class MPSoC:
    def __init__(self, qtNodos, qtTask):
        self.qtNodos = qtNodos
        self.qtTask = qtTask
        self.matrix = self.buildMatriz(qtNodos, qtTask)
        self.nline = 0
        self.ncolumn = 0

        #Note: matrix[x][y] where x = line and y = column
        self.State = "inicial"


    def buildMatriz(self, quant, qtTask):
        nline = math.ceil(math.sqrt(quant))
        ncolumn = math.ceil(quant / nline)

        self.nline = nline
        self.ncolumn = ncolumn

        matrix, line = [], []
        qtTask = qtTask

        for i in range(nline):
            line = []
            for j in range(ncolumn):
                line.append(NodoChaveamento(i, j, qtTask))
            matrix.append(line)

        matrix[0][0] = NodoControle()

        return matrix


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
        if [self.x, self.y] == task.origin:
            self.tasks.append(task)
        else:
            if task.origin[0] < self.x:
                super().matrix[self.x + 1][self.y].recieveLoad(task)
            elif task.origin[0] == self.x and task.origin[1] < self.y:
                super().matrix[self.x][self.y + 1].recieveLoad(task)

        #########!!!!!!! INPUT CONDITION THAT SEND TO THE INDEX 0,0



    def sendLoad(self, task):

        #Register the usage of Nod
        self.count = self.count + task.load

        if [self.x, self.y] == task.destiny:
            print(task)
            print("task executed!")
        else:
            if task.destiny[0] == self.x and task.destiny[1] < self.y:
                super().matrix[self.x][self.y + 1].sendLoad(task)
            elif task.destiny[0] == self.x and task.destiny[1] > self.y:
                super().matrix[self.x][self.y - 1].sendLoad(task)
            elif task.destiny[0] < self.x and task.destiny[1] == self.y:
                super().matrix[self.x + 1][self.y].sendLoad(task)
            elif task.destiny[0] > self.x and task.destiny[1] == self.y:
                super().matrix[self.x - 1][self.y].sendLoad(task)


class NodoControle():
    def __init__(self):
        self.data = ""
        self.progs = {
            "progA" : [Task, Task, Task],
            "progB" : [Task, Task, Task]
        }

    def __str__(self):
        return "Nodo de Controle"


    def readJson(self, localFile):
        self.data = json.load(open(localFile))

    def startProcess(self):

        for key in self.progs:
            x = random.randint(1, super().nline)
            y = random.randint(1, super().ncolumn)
            self.flood_fill(x, y, key)

########
    def is_valid_point(self, nline, ncolumn):
        if nline == 0 and ncolumn == 0:
            return False

        return nline >= 0 and nline < super().nline\
               and ncolumn >= 0 and ncolumn < super().ncolumn

    def is_full(self, line, column):
        return len(super().matrix[line][column].tasks) == super().qtTask

    def have_task(self, key):
        if len(self.progs.get(key)) > 0:
            return True
        else:
            return False

    def allocateTask(self, key):
        super().matrix[0][1].recieveLoad(self.progs.get(key)[0])
        self.progs.get(key).pop(0)

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
        return neighbors

    def flood_fill(self, line, column, key):

        if not self.have_task(key):
            return

        if self.is_full(line, column):
            return

        self.allocateTask(key)

        neighbors = self.get_neighbors(line, column)

        for neighbor in neighbors:
            self.flood_fill(neighbor[0], neighbor[1], key)