import math
import numpy as np
import random
import timeit
import matplotlib.pyplot as plt

class CS :
    def __init__(self, nestCount, pa, pc, problem):
        self.nestCount = nestCount # counts of nest
        self.pa = pa # Probabilty of abandon
        self.generation = 0 # current generation
        self.nests = [] # nest set
        self.fitness = [] # fitness set
        self.pc = pc # How much smart this cuckoo??
        self.population = [] # 2-dimentional population set[nest, fitness]
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

    def levyFlight(self):
        # u의 세제곱근분의 1
        return math.pow(random.uniform(0.0001, 0.9999), -1.0 / 3.0)

    def swap(self, route, i, j):
        temp = route[i]
        route[i] = route[j]
        route[j] = temp
        return route

    def levyTwoOpt(self, nest, a, c):
        nest = nest[:]
        new_nest = self.swap(nest, a, c)
        return new_nest

    def levyDoublebridge(self, nest, a, b, c, d):
        nest = nest[:]
        new_nest = self.swap(nest, a, b)
        new_nest = self.swap(new_nest, b, d)
        return new_nest

    def search(self):
        self.make_distDataframe(self.problem)
        # Init nests
        for i in range(self.nestCount):
            self.nests.append(random.sample(range(0, self.cities_count), self.cities_count))
            self.fitness.append(round(self.cal_fit(self.nests[i]), 5))

        self.population = np.array([self.nests, self.fitness])
        self.population = self.population.T
        self.population = self.population[np.argsort(self.population[:, 1])]
        print('초기화 최대 해 : \n', self.population[0, 0], "\n", self.population[0, 1])

        while 1 :
            self.generation += 1

            # Get a cuckoo randomly by levy flight
            cuckooNest = self.population[random.randint(0, int(self.pc*self.nestCount)), 0]
            if self.levyFlight():
                cuckooNest = self.levyDoublebridge(cuckooNest, random.randint(0, self.cities_count - 1),
                                              random.randint(0, self.cities_count - 1)
                                              , random.randint(0, self.cities_count - 1),
                                              random.randint(0, self.cities_count - 1))
            else:
                cuckooNest = self.levyTwoOpt(cuckooNest, random.randint(0, self.cities_count - 1),
                                        random.randint(0, self.cities_count - 1))
            randomNestIndex = random.randint(0, self.nestCount - 1)

            # Evaluate and replace
            if (self.population[randomNestIndex, 1] > self.cal_fit(cuckooNest)):
                self.population[randomNestIndex, 0] = cuckooNest
                self.population[randomNestIndex, 1] = self.cal_fit(cuckooNest)

            # Pa of worse nests are abandoned and new ones built
            for i in range(self.nestCount - int(self.pa*self.nestCount), self.nestCount):
                self.population[i, 0] = self.levyTwoOpt(self.population[i, 0], random.randint(0, self.cities_count - 1),
                                               random.randint(0, self.cities_count - 1))
                self.population[i, 1] = self.cal_fit(self.population[i, 0])
            self.population = self.population[np.argsort(self.population[:, 1])]

            if self.generation % 5000 == 0:
                print(self.generation, '세대 최적 해 : \n', self.population[0, 1])
                print(self.population[0, 0])

                plotData = []
                for index in self.population[0, 0]:
                    plotData.append([round(float(cs.dots_list[int(index)].split(" ")[0]), 3),
                                     round(float(cs.dots_list[int(index)].split(" ")[1]), 3)])
                plotData = np.array(plotData)
                plotData = plotData.T

                textStr = "fitness :", self.population[0, 1]

                plt.plot(plotData[0], plotData[1])
                plt.text(0.05, 0.95, textStr, fontsize=20, fontweight='bold')
                plt.show()

if __name__ == "__main__" :
    cs = CS(nestCount=20, pa=0.25, pc=0.6, problem="dots/cycle51.in")
    cs.search()