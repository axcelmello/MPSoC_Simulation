from MPSoC import MPSoC

teste = MPSoC(9, 2)

teste.matrix[0][0].startProcess()
teste.matrix[0][0].executeTasks()
teste.showMatrixUsage()








#print()
#for line in range(3):
#    for column in range(3):
#        print(teste.matrix[line][column].tasks, " -> ", line, column)
#print(teste.matrix[0][0].progs)


if __name__ == '__main__':
    print()
    print("end")