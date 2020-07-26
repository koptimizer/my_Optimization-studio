import math
import numpy as np
import random
import timeit

class CS :
    def __init__(self, nestCount, pa, stepSize, ranges, convergence):
        self.nestCount = nestCount # counts of nest
        self.pa = pa # Probabilty of discoverd
        self.generation = 0 # current generation
        self.nests = [] # nest set
        self.fitness = [] # fitness set
        self.stepSize = stepSize # step size 'a'
        self.ranges = [ranges*-1, ranges] # problem ranges
        self.populations = [] # 2-dimentional population set[nest, fitness]
        self.convergence = convergence # Convergence rate [0~1]
        self.finder = 0 # first global optimal
        self.finderBools = False

    def ackleyFunc(self, x, y):
        # optimal point == min(0, 0) = 0
        z = -20 * math.exp(math.fabs(-0.2 * math.sqrt(0.5 * (x ** 2 + y ** 2)))) - math.exp(
            math.fabs(0.5 * (math.cos(2 * x * math.pi) + math.cos(2 * y * math.pi)))) + math.e + 20
        return math.fabs(z)

    def levyFlight(self):
        # u의 세제곱근분의 1
        return math.pow(random.uniform(0.0001, 0.9999), -1.0 / 3.0)

    def search(self):
        # Init nests
        for i in range(self.nestCount):
            X = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
            Y = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
            self.fitness.append(round(self.ackleyFunc(X, Y), 4))
            self.nests.append(np.array([X, Y]))

        populations = np.array([self.nests, self.fitness])
        populations = populations.T
        self.populations = populations[np.argsort(populations[:, 1])]
        print('초기화 최대 해 : \n', self.populations[0, 0], "\n", self.populations[0, 1])

        while 1:
            self.generation += 1
            populations = self.populations.copy()
            # Get a cuckoo randomly by levy flight
            cuckooNest = populations[random.randint(0, self.nestCount - 1), 0]
            similarity = self.levyFlight()
            cuckooNest = np.array([round(cuckooNest[0]+self.stepSize*similarity, 6), round(cuckooNest[1]+self.stepSize*similarity, 6)])
            randomNestIndex = random.randint(0, self.nestCount - 1)

            # Evaluate and replace
            if (populations[randomNestIndex, 1] > self.ackleyFunc(cuckooNest[0], cuckooNest[1])):
                populations[randomNestIndex, 0] = cuckooNest
                populations[randomNestIndex, 1] = round(self.ackleyFunc(cuckooNest[0], cuckooNest[1]), 4)

            # Pa of worse nests are abandoned and new ones built
            for i in range(self.nestCount - int(self.pa * self.nestCount), self.nestCount):
                X = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
                Y = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
                populations[i, 0] = np.array([X, Y])
                populations[i, 1] = round(self.ackleyFunc(X, Y), 4)
            self.populations = populations[np.argsort(populations[:, 1])]

            if self.generation % 50000 == 0:
                print(self.generation, '세대 최적 해 : \n', self.populations[0, 1])
                print(self.populations[0, 0])
                print(self.populations)

            # satisfied?
            if self.populations[0,1] == 0 and self.finderBools == False :
                self.finder = self.generation
                self.finderBools = True
            if self.populations[0,1] == self.populations[int(self.nestCount*self.convergence), 1] :
                print("최적 해 :", self.populations[0, 0], self.populations[0, 1])
                print("첫 수렴 :", self.finder)
                print(self.generation, "수렴 완료")
                break

if __name__ == "__main__" :
    cs = CS(20, 0.25, 1, 5, 0.2)
    start = timeit.default_timer()
    cs.search()
    stop = timeit.default_timer()
    print("시간 :", stop - start)
