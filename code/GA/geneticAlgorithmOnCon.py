import math
import timeit
import numpy as np
import random

class GA():
    def __init__(self, selectionPressure, mutationProbability, chromosomeCount, SelectionProbability, ranges, convergence):
        self.selPs = selectionPressure
        self.mutPa = mutationProbability
        self.chrCount = chromosomeCount
        self.selPa = SelectionProbability
        self.ranges = [ranges*-1, ranges]
        self.gene = []
        self.fitness = []
        self.population = [[],[]]
        self.generation = 0
        self.convergence = convergence  # Convergence rate [0~1]
        self.finder = 0  # first global optimal
        self.finderBools = False

    def ackleyFunc(self, x, y):
        # optimal point == min(0, 0) = 0
        z = -20 * math.exp(math.fabs(-0.2 * math.sqrt(0.5 * (x ** 2 + y ** 2)))) - math.exp(
            math.fabs(0.5 * (math.cos(2 * x * math.pi) + math.cos(2 * y * math.pi)))) + math.e + 20
        return math.fabs(z)

    def randomTwo(self, ranges):
        randomList = []
        randomList += random.sample(range(0, ranges), 2)
        randomList.sort()
        return randomList

    def evolution(self) :
        # init choromosomes
        for i in range(self.chrCount):
            X = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
            Y = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
            self.fitness.append(round(self.ackleyFunc(X, Y), 4))
            self.gene.append(np.array([X, Y]))

        self.population = np.array([self.gene, self.fitness])
        self.population = self.population.T
        self.population = self.population[np.argsort(self.population[:, 1])]
        print('초기화 최대 해 : \n', self.population[0, 0], "\n", self.population[0, 1])

        while 1:
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
                # crossover : means crossover
                daddy_value = self.population[parents_index[0], 0].copy()
                mommy_value = self.population[parents_index[1], 0].copy()
                offspring = np.array([round((daddy_value[0]+mommy_value[0])/2, 6), round((daddy_value[1]+mommy_value[1])/2, 6)])
                offspring_fit = round(self.ackleyFunc(offspring[0], offspring[1]), 4)

                # mutation : random exchange mutation
                mut_p = random.random()
                if mut_p < self.mutPa:
                    X = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
                    Y = round(random.uniform(self.ranges[0], self.ranges[1]), 6)
                    offspring = np.array([X, Y])
                    offspring_fit = round(self.ackleyFunc(X, Y), 4)
                offsprings.append(np.array([offspring, offspring_fit]))
            self.population = np.vstack((self.population, offsprings))

            # Replacement
            self.population = self.population[np.argsort(self.population[:, 1])]
            for i in range(int(self.chrCount*self.selPa)) :
                self.population = np.delete(self.population, len(self.population)-1, axis=0)
            if self.generation % 1 == 0:
                print(self.generation, '세대 최적 해 : \n', self.population[0, 1])
                print(self.population)

            # Satisfied?
            if self.population[0,1] == 0 and self.finderBools == False :
                self.finder = self.generation
                self.finderBools = True
            if self.population[int(self.chrCount*self.convergence), 1] == 0 :
                print("최적 해 :", self.population[0, 0], self.population[0, 1])
                print("첫 수렴 :", self.finder)
                print(self.generation, "수렴 완료")
                break

if __name__ == "__main__":
    ga = GA(0.7, 0.2, 20, 0.5, 5, 0.2)
    start = timeit.default_timer()
    ga.evolution()
    stop = timeit.default_timer()
    print("시간 :", stop - start)