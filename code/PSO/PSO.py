import numpy as np
import random
import math

class Swarm :
    def __init__(self, n, range, acceleratingConstant):
        self.particles = n # 입자의 수
        self.acceleratingConst = acceleratingConstant # 가속상수
        self.range = [range*-1, range] # 입자의 이동범위
        self.swarm = [] # 군집의 해집단
        self.indivisualBest = 0 # 입자의 최적해
        self.swarmBest = 0 # 군집의 최적해

    def swarmInit(self):
        for n in range(self.particles):
            swarmX = random.uniform(self.range[0], self.range[1])
            swarmY = random.uniform(self.range[0], self.range[1])
            self.swarm.append([swarmX, swarmY])

    def move(self, particle):
        for n in range(self.particles) :
            swarmX = (self.swarm[n])[0]
            swarmY = (self.swarm[n])[1]




class Environment :
    def __init__(self, range):
        self.range = range
    def matyasFunc(self, x, y):
        # min(0, 0) = 0
        if x < self.range*-1 or x > self.range or y < self.range*-1 or y > self.range*-1:
            print("Input Error range : -5 ~ 5")
            exit(1)
        else:
            z = 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y
            return z

    def himmelblauFunc(self, x, y):
        # min(3, 2) = 0
        # min(-2.805118, 3.131312) = 0
        # min(-3.779310, -3.283186) = 0
        # min(3.584428, -1.848126) = 0
        if x < self.range*-1 or x > self.range or y < self.range*-1 or y > self.range:
            print("Input Error range : -5 ~ 5")
            exit(1)
        else:
            z = (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2
            return round(z, 10)
