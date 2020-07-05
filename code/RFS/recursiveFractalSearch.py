import math
import numpy as np
import random
import timeit
from threading import Thread
import functools

dist_ar = []  # 거리표(global)
cities_count = 0  # 도시 수(global)
dots_list = []  # 도시 리스트(global)

# Hyper Parameter
limits = 60 * 12 # 제한시간
Fractal_size = 5 # 재귀 수

# 시간제한 데코레이터
def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds_before_timeout))]

            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e

            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except Exception as e:
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret

        return wrapper

    return deco

# 거리표 제작(param : 문제 경로)
def make_distArray(str):
    global dist_ar
    global limit_time
    global cities_count
    global dots_list

    reader = open(str, mode='rt', encoding='utf-8')
    dots_list = reader.read().split("\n")  # ['x1 y1', 'x2 y2', 'x3 y3' ... 'xn yn']
    cities_count = int(dots_list.pop(0))

    x_list = []  # ['x1', 'x2', 'x3' ... 'xn']
    y_list = []  # ['y1', 'y2', 'y3' ... 'yn']
    for i in range(cities_count):
        temp = dots_list[i].split(" ")
        x_list.append(float(temp[0]))
        y_list.append(float(temp[1]))

    dist_ar = []
    for n in range(cities_count):
        temp = []
        for m in range(cities_count):
            temp.append((math.sqrt(((x_list[m] - x_list[n]) ** 2) + ((y_list[m] - y_list[n]) ** 2))))
        dist_ar.append(temp)

    dist_ar = np.array(dist_ar)
    print(dist_ar)

# 거리표를 이용한 적합도 매칭 함수
def cal_fit(stri):
    fit = 0
    for steps in range(len(stri) - 1):
        fit += dist_ar[stri[steps], stri[steps + 1]]
    return fit

def optFunc(stri) :
    route = stri
    fitness = cal_fit(route)
    while 1 :
        breaker = True
        for i in range(len(route)):
            for j in range(len(route)):
                new_route = optSwap(route, i, j)
                new_fitness = cal_fit(new_route)
                if new_fitness < fitness:
                    route = new_route
                    fitness = new_fitness
                    breaker = False
                    break
            if breaker == False :
                break
        if breaker == True :
            break
    return route

def optSwap(route,head,tail):
    new_route = []
    new_route += route[0:head]
    new_route += reversed(route[head:tail+1])
    new_route += route[tail+1:len(route)]
    return new_route

def randomTwo(ranges) :
    randomList = []
    randomList += random.sample(range(0,ranges), 2)
    randomList.sort()
    return randomList

def randomFour(ranges) :
    randomList = []
    randomList += random.sample(range(0,ranges), 4)
    randomList.sort()
    return randomList

def twoOptMove(nest, pointList) :
    nest = nest[:]
    new_nest = optSwap(nest, pointList[0], pointList[1])
    return new_nest

def doublebridgeMove(nest, pointList) :
    nest = nest[:]
    new_nest = optSwap(nest, pointList[0], pointList[1])
    new_nest = optSwap(new_nest, pointList[1], pointList[3])
    return new_nest

def makeFractal(route, calls) :
    global population
    if not calls > Fractal_size :
        calls += 1
        small = twoOptMove(route, sorted(randomTwo(cities_count)))
        large = doublebridgeMove(route, sorted(randomFour(cities_count)))
        population.append(small)
        population.append(large)
        makeFractal(small, calls)
        makeFractal(large, calls)

def makeArr(population) :
    fits = []
    for i in range(len(population)) :
        fits.append(cal_fit(population[i]))
    arr = np.array([population, fits])
    return arr.T

@timeout(limits)
def run() :
    global population
    generation = 0
    optSol = random.sample(range(0, cities_count), cities_count)
    population.append(optSol)
    calls = 0
    while 1 :
        makeFractal(optSol, calls)
        population = makeArr(population)
        population = population[np.argsort(population[:, 1])] # fitness 기준 정렬
        optSol = population[0,0]
        if generation % 5000 == 0 :
            print(generation, "세대 최적해", population[0,1])
        population = []
        population.append(optSol)
        generation += 1
        calls = 0


population = [] # 전역변수로 선언한 것
try :
    make_distArray("dots/opt_cycle200.in")
    start = timeit.default_timer()
    run()
    stop = timeit.default_timer()
    print(stop - start)
except :
    stop = timeit.default_timer()
    print(stop - start)