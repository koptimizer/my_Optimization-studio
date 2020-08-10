import math
import timeit
import numpy as np
import random

class GA :
    def __init__(self, populationSize, selectionProbability, threshold, mutationProbability):
        self.job = ['j1', 'j2']
        self.operation = [['o11', 'o12'],
                          ['o21', 'o22', 'o23']]
        self.machine = [[2, 999, 3, 4, 999],
                        [6, 8, 999, 6, 7],
                        [5, 999, 6, 5, 11],
                        [3, 4, 999, 999, 5],
                        [4, 999, 5, 999, 8]]
        self.populationSize = populationSize
        self.selectionProbability = selectionProbability
        self.mutationProbability = mutationProbability
        self.threshold = threshold
        self.chromosome = []
        self.fitness = []
        self.population = [[], []]

    def getFitness(self, schedule) :
        fitness = 0
        return fitness

    def selectMachine(self, operation) :
        alt = self.machine[operation]


    def globalSelectionInit(self) :
        ms = []
        ta = []
        msSize = 0
        for j in range(len(self.job)) :
            for o in range(len(self.operation[j])) :
                msSize += 1
        for i in range(msSize) :
            ms.append(0)
            ta.append(0)

        for i in range(msSize) :
              available = []
            for mac in self.machine :
                available.append(mac[i]+ta[i])


    def evolution(self) :
        for i in range(self.populationSize) :
            ms = self.globalSelectionInit()


if __name__ == "__main__" :
    ga = GA(populationSize=20, selectionProbability=0.5, threshold=0.7, mutationProbability=0.1)
    ga.evolution()