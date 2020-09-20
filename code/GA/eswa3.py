import numpy
import random
import pandas as pd
pd.set_option('display.expand_frame_repr', False) # DataFrame 출력시 짤림 해결
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)

'''
j1 = [o11, o12] = [[2, 6, 5, 3, 4], [n, 8, n, 4, n]]
j2 = [o21, o22, o23] = [[3, n, 6, n, 5], [4, 6, 5, n, n], [n, 7, 11, 5, 8]]
'''

# 문제마다 바뀌는 것
# jobs, available, seq

class GA :
    def __init__(self, populationSize, crossoverProbability, iterationNumber, mutationProbability):
        self.populationSize = populationSize
        self.iterationNumber = iterationNumber
        self.jobs = [[2, 6, 5, 3, 4], [None, 8, None, 4, None], [3, None, 6, None, 5], [4, 6, 5, None, None], [None, 7, 11, 5, 8]]
        self.population = [] # [[Machine Selection], [Operation Sequence], [Allocation], [fitness]]
        # elf.schedule = []
        # self.chromosome = [[4, 1, 2, 2, 4], [2, 2, 1, 1, 2]] # 폼
        # self.machine = {1 : [], 2 : [], 3 : [], 4 : [], 5 : []} # 폼
        self.available = [5, 2, 3, 3, 4] # 각 operation이 접근가능한 machine의 max(index)
        self.seq = [[2, 1], [5, 4, 3]] # 각 job의 operation들이 pop을 위해 거꾸로 들어있음
        self.crossoverProbability = crossoverProbability
        self.mutationProbability = mutationProbability

    def init(self):
        # RS
        for iter in range(self.populationSize) :
            chromosome = []
            temp = []
            # Machine Selection part
            for i in self.available :
                temp.append(random.randint(1, i))
            chromosome.append(temp) # MS

            # Operation Sequence part
            temp = [1, 1, 2, 2, 2]
            random.shuffle(temp)
            chromosome.append(temp) # OS
            chromosome.append(self.encoding(chromosome)) # MF
            chromosome.append(self.cal_fit(chromosome)) # FN
            self.population.append(chromosome)
        # self.population = sorted(self.population, key=lambda x: x[3])

    # get Machine Form
    def encoding(self, chromosome):
        print(chromosome)
        machine = {1 : [], 2 : [], 3 : [], 4 : [], 5 : []}
        sequencer = []
        for i in chromosome[1] :
            sequencer.append(self.seq[i-1].pop())
        # print(sequencer) # 확인용
        os = {1 : 0, 2 : 0}
        for i, j in zip(sequencer, chromosome[1]) : # 1~5, 1~2
            i = i-1
            countNone = 0
            picker = -1
            for pos in range(chromosome[0][i]) :
                if self.jobs[i][pos] == None :
                    countNone += 1
                try:
                    if pos == max(range(chromosome[0][i])) and pos != 0 and self.jobs[i][pos+1] == None and self.jobs[i][pos-1] == None :
                        countNone +=1
                except:
                    pass

            '''
            j1 = [o11, o12] = [[2, 6, 5, 3, 4], [n, 8, n, 4, n]]
            j2 = [o21, o22, o23] = [[3, n, 6, n, 5], [4, 6, 5, n, n], [n, 7, 11, 5, 8]]
            '''

            temp = self.jobs[i][chromosome[0][i] - 1 + countNone]
            if sum(machine[chromosome[0][i]]) == 0 and os[j] == 0 :
                os[j] += sum(machine[chromosome[0][i]])
                if picker != j and picker != -1:
                    machine[chromosome[0][i] + countNone].append(os[j] + os[picker])
                elif picker == j and picker != -1:
                    machine[chromosome[0][i] + countNone].append(os[j])
                else:
                    machine[chromosome[0][i] + countNone].append(os[j])
                machine[chromosome[0][i] + countNone].append(temp)
            elif sum(machine[chromosome[0][i]]) == 0 and os[j] != 0 :
                if sum(machine[chromosome[0][i]]) < os[j] :
                    idle = os[j] - sum(machine[chromosome[0][i]])
                    if idle <= 0 :
                        machine[chromosome[0][i] + countNone].append(os[j])
                    else :
                        machine[chromosome[0][i] + countNone].append(idle + os[j])
                        os[j]+=idle
                        os[j]-=temp
                    machine[chromosome[0][i] + countNone].append(temp)
                else :
                    machine[chromosome[0][i] + countNone].append(os[j])
                    machine[chromosome[0][i] + countNone].append(temp)

            elif sum(machine[chromosome[0][i]]) != 0 and os[j] == 0 :
                if picker != j and picker != -1:
                    machine[chromosome[0][i] + countNone].append(os[j]+os[picker])
                elif picker == j and picker != -1 :
                    machine[chromosome[0][i] + countNone].append(os[j])
                else :
                    machine[chromosome[0][i] + countNone].append(os[j])
                os[j] += sum(machine[chromosome[0][i] + countNone])
                machine[chromosome[0][i] + countNone].append(temp)

            elif sum(machine[chromosome[0][i]]) != 0 and os[j] != 0 :
                if sum(machine[chromosome[0][i]]) < os[j] :
                    idle = os[j] - sum(machine[chromosome[0][i]])
                    machine[chromosome[0][i] + countNone].append(idle)
                    machine[chromosome[0][i] + countNone].append(temp)
                else :
                    machine[chromosome[0][i] + countNone].append(os[j])
                    machine[chromosome[0][i] + countNone].append(temp)

            picker = j
            os[j] += temp
            print(machine)
            print(os)
        self.seq = [[2, 1], [5, 4, 3]] # 원상복구
        print()
        return machine

    # get Fitness
    def cal_fit(self, chromosome):
        processTimes = []
        for machine in range(len(self.available)) :
            processTimes.append(sum(chromosome[2][machine+1]))
        return max(processTimes)

    def randomTwo(self, ranges):
        randomList = []
        randomList += random.sample(range(0, ranges), 2)
        randomList.sort()
        return randomList

    def crossover(self):
        # MS part
        for pop in range(self.populationSize):
            parents = self.randomTwo(len(self.population[pop]))
            points = self.randomTwo(len(self.population[0][0]))
            if random.random() <= self.crossoverProbability:
                offspring1 = []
                offspring2 = []
                if random.random() >= 0.5:
                    # two-point crossover
                    daddy = self.population[parents[0]][0].copy()
                    mommy = self.population[parents[1]][0].copy()
                    temp = daddy[points[0]:points[1]].copy()
                    daddy[points[0]:points[1]] = mommy[points[0]:points[1]]
                    mommy[points[0]:points[1]] = temp
                    offspring1.append(daddy)
                    offspring2.append(mommy)
                else:
                    # uniform crossover
                    daddy = self.population[parents[0]][0].copy()
                    mommy = self.population[parents[1]][0].copy()
                    temp = daddy[points[0]:points[1]]
                    temp = daddy.copy()
                    daddy[points[0]] = mommy[points[0]]
                    daddy[points[1]] = mommy[points[1]]
                    mommy[points[0]] = temp[points[0]]
                    mommy[points[1]] = temp[points[1]]
                    offspring1.append(daddy)
                    offspring2.append(mommy)
                # OS part
                # todo Operation sequence
                offspring1.append(self.population[parents[0]][1])
                offspring2.append(self.population[parents[1]][1])
                offspring1.append(self.encoding(offspring1))
                offspring2.append(self.encoding(offspring2))
                offspring1.append(self.cal_fit(offspring1))
                offspring2.append(self.cal_fit(offspring2))
                self.population.append(offspring1)
                self.population.append(offspring2)
            else:
                pass

    def mutation(self, chromosome):
        # todo
        pass

    def evaluate(self):
        self.population = sorted(self.population, key=lambda x : x[3])
        del self.population[50:]

    def simulation(self):
        self.init()
        # for iter in range(self.iterationNumber) :
        #     self.crossover()
        #     self.evaluate()
        self.population = pd.DataFrame(self.population)
        print(self.population.iloc[0][2])
        print(self.population)


if __name__ == "__main__" :
    ga = GA(populationSize=50, iterationNumber=100, crossoverProbability=0.7, mutationProbability=0.01)
    ga.simulation()