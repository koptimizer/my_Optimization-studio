import math
import numpy as np
import random
import timeit
import matplotlib.pyplot as plt

class CS :
    def __init__(self, nestCount, pa, stepSize, ranges):
        self.nestCount = nestCount # count of nests
        self.pa = pa # Probability of discovered
        self.generation = 0 # current generation
        self.nests = [] # nests set
        self.fitness = [] # fitness set
        self.stepSize = stepSize # step size 'a'
        self.ranges = [ranges*-1, ranges] # problem ranges
        self.population = [] # [nests, fitness] set

    def ackleyFunc(self, x, y):
        # optimal point == min(0, 0) = 0
        z = -20 * math.exp(math.fabs(-0.2 * math.sqrt(0.5 * (x ** 2 + y ** 2)))) - math.exp(
            math.fabs(0.5 * (math.cos(2 * x * math.pi) + math.cos(2 * y * math.pi)))) + math.e + 20
        return math.fabs(z)

    def levyFlight(self):
        # u의 세제곱근분의 1
        return math.pow(random.uniform(0.0001, 0.9999), -1.0 / 3.0)

    def visualize(self):
        data = self.population[:, 0].copy()
        x = []
        y = []
        for i in range(len(self.population)) :
            x.append(data[i][0])
            y.append(data[i][1])
        plt.plot(x, y, 'ro')
        plt.axis([self.ranges[0], self.ranges[1], self.ranges[0], self.ranges[1]])
        plt.show()

    def search(self):
        # Init nests
        for i in range(self.nestCount):
            X = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
            Y = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
            self.fitness.append(round(self.ackleyFunc(X, Y),4))
            self.nests.append(np.array([X, Y]))

        self.population = np.array([self.nests, self.fitness])
        self.population = self.population.T # transpose matrix
        self.population = self.population[np.argsort(self.population[:, 1])] # sorting
        print('초기화 최대 해 : \n', self.population[0, 0], "\n", self.population[0, 1])
        self.visualize()

        while self.generation < 10000:
            self.generation += 1
            # Get a cuckoo randomly by levy flight
            cuckooNest = self.population[random.randint(0, self.nestCount - 1), 0]
            levyX = self.levyFlight()
            levyY = self.levyFlight()
            cuckooNest = np.array([round(cuckooNest[0]+self.stepSize*levyX, 6), round(cuckooNest[1]+self.stepSize*levyY, 6)])
            randomNestIndex = random.randint(0, self.nestCount - 1)

            # Evaluate and replace
            if (self.population[randomNestIndex, 1] > self.ackleyFunc(cuckooNest[0], cuckooNest[1])):
                self.population[randomNestIndex, 0] = cuckooNest
                self.population[randomNestIndex, 1] = self.ackleyFunc(cuckooNest[0], cuckooNest[1])

            # Pa of worse nests are abandoned and new ones built
            for i in range(self.nestCount - int(self.pa * self.nestCount), self.nestCount):
                X = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
                Y = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
                self.population[i, 0] = np.array([X, Y])
                self.population[i, 1] = round(self.ackleyFunc(X, Y), 4)
            self.population = self.population[np.argsort(self.population[:, 1])]

            if self.generation % 500 == 0:
                print(self.generation, '세대 최적 해 : \n', self.population[0, 1])
                print(self.population[0, 0])
                print(self.population)
                self.visualize()

if __name__ == "__main__" :
    cs = CS(100, 0.25, 1, 5)
    start = timeit.default_timer()
    cs.search()
    stop = timeit.default_timer()
    print(stop - start)
