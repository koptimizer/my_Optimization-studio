import math
import timeit
import numpy as np
import random

class GA :
    def __init__(self, populationSize, selectionProbability, threshold, mutationProbability):
        self.job = ['j1', 'j2']
        self.operation = [['o11', 'o22'],
                          ['o21', 'o22', 'o23']]
        self.machine = {'o11' : [2, 6, 5, 3, 4],
                        'o12' :[999, 8, 999, 4, 999],
                        'o21' : [3, 999, 6, 999, 5],
                        'o22' :[4, 6, 5, 999, 999],
                        'o23' : [999, 7, 11, 5, 8]}
        self.operations = 5
        self.populationSize = populationSize
        self.selectionProbability = selectionProbability
        self.mutationProbability = mutationProbability
        self.threshold = threshold
        self.chromosome = []
        self.fitness = []
        self.population = [[], []]

    def getFitness(self, chromosome) :
        fitness = 0
        ms = chromosome[0]
        os = chromosome[1]
        temp_oper = self.operation
        real_os = []
        real_pTime = [0, 0, 0, 0, 0]

        for o in range(self.operations) :
            real_os.append(temp_oper[os[o]-1].pop(0))

        for o in range(real_os) :
            real_ms = [0, 0]
            for i in range(real_os) :
                print()
                # TODO: O_ij가 ms에 따라 상대적 할당될 시 pTime-> real_ms[0], 절대적 할당경로 -> real_ms[1]


        fitness += self.machine[o][real_ms[0]]
        real_pTime[real_ms[1]] += self.machine[o][real_ms[0]]

        return fitness

    def selectMachine(self, operation) :
        alt = self.machine[operation]

    def globalSelectionInit(self) :
        print()
        # TODO : GS부

    def localSelectionInit(self):
        print()
        # TODO : ls부

    def evolution(self) :
        # TODO : Init부
        # TODO : Crossover부
        # TODO : Muatate부

        print(self.getFitness([[4,1,2,2,4],[2,2,1,1,2]]))

if __name__ == "__main__" :
    ga = GA(populationSize=20, selectionProbability=0.5, threshold=0.7, mutationProbability=0.1)
    ga.evolution()