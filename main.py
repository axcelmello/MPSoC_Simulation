from MPSoC import MPSoC

teste = MPSoC(9, 2)

for line in range(3):
    for column in range(3):
        print(teste.matrix[line][column])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("end")