import numpy
import random

'''
j1 = [o11, o12] = [[2,6,5,3,4], [n, 8, n, 4, n]]
j2 = [o21, o22, o23] = [[3, n, 6, n, 5], [4, 6, 5, n, n], [n, 7, 11, 5, 8]]
'''

class GA :
    def __init__(self):
        self.jobs = [[2, 6, 5, 3, 4], [None, 8, None, 4, None], [3, None, 6, None, 5], [4, 6, 5, None, None], [None, 7, 11, 5, 8]]
        self.population = []
        self.chromosome = [[4, 1, 2, 2, 4], [2, 2, 1, 1, 2]]
        self.machine = {1 : [], 2 : [], 3 : [], 4 : [], 5 : []}
        self.seq = [[2, 1], [5, 4, 3]]

    def encoding(self):
        # selector = []
        sequencer = []
        for i in self.chromosome[1] :
            sequencer.append(self.seq[i-1].pop())
        print(sequencer)

        for i in sequencer :
            i = i-1
            countNone = 0
            for j in range(self.chromosome[0][i]) :
                if self.jobs[i][j] == None :
                    countNone += 1

            temp = self.jobs[i][self.chromosome[0][i]-1+countNone]
            self.machine[self.chromosome[0][i]+countNone].append(temp)
        print(self.machine)
        return self.machine

    def crossover(self, population):
        # todo
        pass

    def mutation(self, chromosome):
        # todo
        pass

    def simulation(self, schedule):
        # todo
        pass

if __name__ == "__main__" :
    ga = GA()
    ga.simulation()