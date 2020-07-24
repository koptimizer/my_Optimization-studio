import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math

class Swarm :
    def __init__(self, n, spaceRange, inertia, ac1, ac2):
        self.particles = n # 입자의
        self.acceleratingFactor1 = ac1 # 군집용 가속상수
        self.acceleratingFactor2 = ac2 # 입자용 가속상수
        self.range = [spaceRange*-1, spaceRange] # 입자의 이동범위
        self.swarm = [] # 군집내 입자 집합
        # self.maxInertia = 0.9 # 관성하중 최대치
        # self.minInertia = 0.4 # 관성하중 최소치
        self.inertia = inertia
        self.swarmBest = [0, 100000] # 군집의 최적해
        self.particleBest = [] # 입자별 최적해 집합

    def swarmInit(self):
        for n in range(self.particles):
            swarmX = round(random.uniform(self.range[0], self.range[1]), 5)
            swarmY = round(random.uniform(self.range[0], self.range[1]), 5)
            # generates particles
            self.swarm.append(np.array([swarmX, swarmY]))
            # updates particlesBest
            self.particleBest.append(np.array([swarmX, swarmY]))
            # updates swarmBest
            if self.ackleyFunc(swarmX, swarmY) <= self.swarmBest[1] :
                self.swarmBest[0] = np.array([swarmX, swarmY])
                self.swarmBest[1] = round(self.ackleyFunc(swarmX, swarmY), 5)

    def move(self, particleIndex):
        currentPosition = self.swarm[particleIndex]
        sbest = self.swarmBest[0] - currentPosition
        pbest = self.particleBest[particleIndex] - currentPosition
        r = round(random.random(), 3)

        # 관성하중의 정확한 의미?
        resultParticle = self.inertia*currentPosition + self.acceleratingFactor1*r*pbest + self.acceleratingFactor2*r*sbest

        resultFitness = round(self.ackleyFunc(resultParticle[0], resultParticle[1]), 5)
        ibestFitness = round(self.ackleyFunc(self.particleBest[particleIndex][0], self.particleBest[particleIndex][1]), 5)

        # updates particleBest
        if resultFitness <= ibestFitness:
            self.particleBest[particleIndex] = resultParticle

        # updates swarmBest
        if resultFitness <= self.swarmBest[1] :
            self.swarmBest[0] = resultParticle
            self.swarmBest[1] = resultFitness

        # moves particle
        self.swarm[particleIndex] = resultParticle

    def goldsteinPriceFunc(self, x, y):
        # min(0, -1) = 3
        z = ((1 + (x + y + 1) ** 2 * (19 - 14 * x + 3 * (x ** 2) - 14 * y + 6 * x * y + 3 * (y ** 2))) * (
                    30 + (2 * x - 3 * y) ** 2 * (
                        18 - 32 * x + 12 * (x ** 2) + 48 * y - 36 * x * y + 27 * (y ** 2))))
        return z

    def ackleyFunc(self, x, y):
        z = -20 * math.exp(math.fabs(-0.2 * math.sqrt(0.5 * (x ** 2 + y ** 2)))) - math.exp(
            math.fabs(0.5 * (math.cos(2 * x * math.pi) + math.cos(2 * y * math.pi)))) + math.e + 20
        return math.fabs(z)

if __name__ == "__main__" :
    # paramters
    GENERATION = 0
    TERMINATION = 0

    # swarm 초기화
    swarm = Swarm(25, 5, 1, 1, 1)
    swarm.swarmInit()
    print(swarm.swarm)

    data = pd.DataFrame(swarm.swarm)
    data.columns = ['x', 'y']

    scatter = sns.scatterplot(x="x", y="y", data=data)

    plt.xlim(swarm.range[0], swarm.range[-1])
    plt.ylim(swarm.range[0], swarm.range[-1])
    plt.grid()

    plt.show()

    while TERMINATION != 10 or GENERATION != 50 :
        GENERATION = GENERATION + 1
        for iteration in range(swarm.particles) :
            swarm.move(iteration)
        print(GENERATION, ":", swarm.swarmBest)
        print(swarm.swarm)
        print(swarm.particleBest)
        if swarm.swarmBest[1] == 0 :
            TERMINATION = TERMINATION + 1

        # scatter찍기

        data = pd.DataFrame(swarm.swarm)
        data.columns = ['x', 'y']

        scatter = sns.scatterplot(x="x", y="y", data =data)

        plt.xlim(swarm.range[0], swarm.range[-1])
        plt.ylim(swarm.range[0], swarm.range[-1])
        plt.grid()

        plt.show()
