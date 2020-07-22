import numpy as np
import random

class Swarm :
    def __init__(self, n, range, acceleratingConstant):
        self.particles = n # 입자의
        self.acceleratingConst = acceleratingConstant # 가속상수
        self.range = [range*-1, range] # 입자의 이동범위
        self.swarm = [] # 군집내 입자 집합
        self.inertia = [] # 입자별 관성 집합
        self.swarmBest = [0, 100000] # 군집의 최적해
        self.particleBest = [] # 입자별 최적해 집합

    def swarmInit(self):
        for n in range(self.particles):
            swarmX = round(random.uniform(self.range[0], self.range[1]),5)
            swarmY = round(random.uniform(self.range[0], self.range[1]),5)
            # generates particles
            self.swarm.append(np.array([swarmX, swarmY]))
            # updates particlesBest
            self.particleBest.append(np.array([swarmX, swarmY]))
            # updates inertia
            self.inertia.append(0)
            # updates swarmBest
            if self.matyasFunc(swarmX, swarmY) <= self.swarmBest[1] :
                self.swarmBest[0] = np.array([swarmX, swarmY])
                self.swarmBest[1] = self.matyasFunc(swarmX, swarmY)

    def move(self, particleIndex):
        currentPosition = self.swarm[particleIndex]
        inertia = self.inertia[particleIndex]
        sbest = self.swarmBest[0] - currentPosition
        pbest = self.particleBest[particleIndex] - currentPosition
        r = round(random.random(), 5)

        # 관성하중의 정확한 의미?
        resultParticle = inertia*currentPosition + self.acceleratingConst*r*sbest + self.acceleratingConst*r*pbest

        resultFitness = self.matyasFunc(resultParticle[0], resultParticle[1])
        ibestFitness = self.matyasFunc(self.particleBest[particleIndex][0], self.particleBest[particleIndex][1])

        # updates inertia
        self.inertia[particleIndex] = resultParticle - currentPosition

        # updates particleBest
        if resultFitness <= ibestFitness:
            self.particleBest[particleIndex] = resultParticle

        # updates swarmBest
        if resultFitness <= self.swarmBest[1] :
            self.swarmBest[0] = resultParticle
            self.swarmBest[1] = resultFitness

        # moves particle
        self.swarm[particleIndex] = resultParticle

    def matyasFunc(self, x, y):
        # min(0, 0) = 0
        z = 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y
        return z

if __name__ == "__main__" :
    # paramters
    GENERATION = 0

    # swarm 초기화
    swarm = Swarm(20, 5, 1)
    swarm.swarmInit()
    while swarm.swarmBest[1] != 0 :
        GENERATION += 1
        for iteration in range(swarm.particles) :
            swarm.move(iteration)
        print(GENERATION, ":", swarm.swarmBest)
        # print(swarm.particleBest)
        # print(swarm.swarm)




