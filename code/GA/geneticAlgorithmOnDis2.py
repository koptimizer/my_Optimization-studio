import math
import timeit
import numpy as np
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class GA():
    def __init__(self, selectionPressure, mutationProbability, chromosomeCount, selectionProbability, problem):
        self.selPs = selectionPressure # selection pressure
        self.mutPa = mutationProbability # Probabilty of mutation
        self.chrCount = chromosomeCount # size of choromosome
        self.selPa = selectionProbability # selection probabilty
        self.choromosome = [] # choromosome set
        self.fitness = [] # fitness set
        self.population = [[],[]] # [choromosome, fitness] set
        self.generation = 0 # current generation
        self.problem = problem # problem route
        self.dist_ar = [] # [dots_list, dots_list ]distance array
        self.cities_count = 0
        self.dots_list = []
        self.limit_time = 0

    def make_distDataframe(self, problem):
        reader = open(problem, mode='rt', encoding='utf-8')
        self.dots_list = reader.read().split("\n")  # ['x1 y1', 'x2 y2', 'x3 y3' ... 'xn yn']
        self.cities_count = int(self.dots_list.pop(0))
        self.limit_time = float(self.dots_list.pop())

        x_list = []  # ['x1', 'x2', 'x3' ... 'xn']
        y_list = []  # ['y1', 'y2', 'y3' ... 'yn']
        for i in range(self.cities_count):
            temp = self.dots_list[i].split(" ")
            x_list.append(float(temp[0]))
            y_list.append(float(temp[1]))

        for n in range(self.cities_count):
            temp = []
            for m in range(self.cities_count):
                temp.append(round((math.sqrt(((x_list[m] - x_list[n]) ** 2) + ((y_list[m] - y_list[n]) ** 2))), 2))
            self.dist_ar.append(temp)

        self.dist_ar = np.array(self.dist_ar)
        print(self.dist_ar)

    def cal_fit(self, route) :
        fit = 0
        for i in range(len(route)-1) :
            if i == len(route)-1 :
                fit += self.dist_ar[route[i], route[0]]
            else :
                fit += self.dist_ar[route[i], route[i+1]]
        return fit

    def randomTwo(self, ranges):
        randomList = []
        randomList += random.sample(range(0, ranges), 2)
        randomList.sort()
        return randomList

    def evolution(self) :
        # init choromosomes
        self.make_distDataframe(self.problem)

        for i in range(self.chrCount):
            self.choromosome.append(random.sample(range(0, self.cities_count), self.cities_count))

        for i in range(self.chrCount):
            self.fitness.append(round(self.cal_fit(self.choromosome[i]), 5))

        self.population = (np.array([self.choromosome, self.fitness])).T
        self.population = self.population[np.argsort(self.population[:, 1])]
        print('초기화 최적 해 : \n', self.population[0, 0], "\n", self.population[0, 1])

        plotData = []
        for index in self.population[0, 0]:
            plotData.append([round(float(ga.dots_list[int(index)].split(" ")[0]), 3),
                             round(float(ga.dots_list[int(index)].split(" ")[1]), 3)])
        plotData = np.array(plotData)
        plotData = plotData.T

        textStr = "fitness :", self.population[0, 1]

        plt.plot(plotData[0], plotData[1])
        plt.text(0.05, 0.95, textStr, fontsize=20, fontweight='bold')
        plt.show()

        while 1 :
            offsprings = []
            self.generation += 1
            # selection : 토너먼트선택,
            for endSel in range(int(self.chrCount*self.selPa)):
                # 난수룰 발생시켜 해집단 내 두 유전자 선택, 선택난수 발생
                # 선택난수가 선택압보다 작으면 두 유전자 중 좋은 유전자가 선택. 아니면 반대로
                parents_index = [0, 0]
                for i in range(len(parents_index)):
                    selGeneNum = self.randomTwo(self.chrCount)
                    match = random.random()
                    if match < self.selPs:
                        if self.population[selGeneNum[0], 1] < self.population[selGeneNum[1], 1]:
                            parents_index[i] = selGeneNum[0]
                        else:
                            parents_index[i] = selGeneNum[1]
                    else:
                        if self.population[selGeneNum[0], 1] < self.population[selGeneNum[1], 1]:
                            parents_index[i] = selGeneNum[1]
                        else:
                            parents_index[i] = selGeneNum[0]
                # crossover : order-based crossover
                daddy_value = self.population[parents_index[0], 0].copy()
                mommy_value = self.population[parents_index[1], 0].copy()

                CsGeneNum = self.randomTwo(self.cities_count)
                offspring = daddy_value[CsGeneNum[0]: CsGeneNum[1]]
                for i in daddy_value[CsGeneNum[0]: CsGeneNum[1]]:
                    mommy_value.remove(i)
                for i in range(len(offspring)):
                    mommy_value.insert(CsGeneNum[0] + i, offspring[i])
                offspring = mommy_value
                offspring_fit = self.cal_fit(offspring)

                # mutation : exchange mutation
                mut_p = random.random()
                if mut_p < self.mutPa:
                    MtGeneNum = self.randomTwo(self.cities_count)
                    mut_Temp = offspring[MtGeneNum[0]]
                    offspring[MtGeneNum[0]] = offspring[MtGeneNum[1]]
                    offspring[MtGeneNum[1]] = mut_Temp
                    offspring_fit = self.cal_fit(offspring)
                offsprings.append(np.array([offspring, offspring_fit]))
            self.population = np.vstack((self.population, offsprings))

            # Replacement
            self.population = self.population[np.argsort(self.population[:, 1])]
            for i in range(int(self.chrCount*self.selPa)) :
                self.population = np.delete(self.population, len(self.population)-1, axis=0)
            if self.generation % 1000 == 0:
                print(self.generation, '세대 최적 해 : \n', self.population[0, 1])
                print(self.population[0, 0])

                plotData = []
                for index in self.population[0, 0]:
                    plotData.append([round(float(ga.dots_list[int(index)].split(" ")[0]), 3),
                                     round(float(ga.dots_list[int(index)].split(" ")[1]), 3)])
                plotData = np.array(plotData)
                plotData = plotData.T

                textStr = "fitness :", self.population[0, 1]

                plt.plot(plotData[0], plotData[1])
                plt.text(0.05, 0.95, textStr, fontsize=20, fontweight='bold')
                plt.show()

                print(self.generation, '세대 최적 해 : \n', self.population[0, 1])
                print(self.population[0, 0])

if __name__ == "__main__":
    ga = GA(selectionPressure=0.7, mutationProbability=0.2, chromosomeCount=20, selectionProbability=0.5, problem="dots/cycle51.in")
    ga.evolution()