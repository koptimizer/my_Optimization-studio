import math
import timeit
import pandas as pd
import random
from threading import Thread
import functools

dist_ar = [] # 거리표(global)
limit_time = 36 # 제한시간(global)
cities_count = 0 # 도시 수(global)
dots_list = [] # 도시 리스트(global)

# 시간제한 데코레이터
def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' %(func.__name__, seconds_before_timeout))]
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

# Hyper Parameter
MUT = 0.2 # 변이확률
SEL = 0.85 # 선택압
END = 1000 # 최종세대 설정
chrCOUNT = 50 # 해집단 내 염색체 개수
selCOUNT = 25 # selection시 선택되는 상위 염색체의 개수

# 거리표 제작(param : 문제 경로) : dist_df
def make_distDataframe(str):
    global dist_df
    global limit_time
    global cities_count
    global dots_list

    reader = open(str, mode='rt', encoding='utf-8')
    dots_list = reader.read().split("\n")  # ['x1 y1', 'x2 y2', 'x3 y3' ... 'xn yn']
    cities_count = int(dots_list.pop(0))
    limit_time = float(dots_list.pop())

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
            temp.append(round((math.sqrt(((x_list[m] - x_list[n]) ** 2) + ((y_list[m] - y_list[n]) ** 2))), 2))
        dist_ar.append(temp)

    dist_df = pd.DataFrame(dist_ar, columns=dots_list, index=dots_list)
    print(dist_df)

# 거리표를 이용한 적합도 매칭 함수
def cal_fit(stri) :
    fit = 0
    for i in range(len(stri)-1) :
        fit += dist_df.iloc[stri[i],stri[i+1]]
    return fit

# 0 ~ ranges-1의 범위 중 두 개를 랜덤으로 샘플링해서 list 리턴
def randomTwo(ranges) :
    randomList = []
    randomList += random.sample(range(0,ranges), 2)
    randomList.sort()
    return randomList

def TSP_GA() :
    # 환경 설정 및 초기화
    generation = 0  # 현재 세대
    population = [] # 현재 세대 or initializing시 최종 population
    population_fit = [] # population의 적합도
    populations = [] #population과 적합도로 이루어진 이차원 배열
    step_result = [] # step을 거칠 때 변화된 population

    # initialize
    for i in range(chrCOUNT) :
        population.append(random.sample(range(0, cities_count), cities_count))

    for i in range(chrCOUNT) :
        population_fit.append(round(cal_fit(population[i]), 5))

    populations = pd.DataFrame([population, population_fit], index = ["chromosome", "fitness"])
    populations = populations.T
    # print('초기 염색체 : \n', population, '\n염색체 별 적합도 :\n', population_fit)
    print(populations)
    while 1 :
        generation += 1
        # selection : 토너먼트선택,
        populations.sort_values(by=['fitness'], inplace=True)
        populations.reset_index(drop=True, inplace=True)
        # print(endGen, '번째 selection 결과 : \n', populations)
        for endSel in range(selCOUNT) :
            # 난수룰 발생시켜 해집단 내 두 유전자 선택, 선택난수 발생
            # 선택난수가 선택압보다 작으면 두 유전자 중 좋은 유전자가 살아남음. 아니면 반대로
            parents_index = [0]*2
            for i in range(len(parents_index)):
                selGeneNum = randomTwo((chrCOUNT - endSel))
                match = random.random()
                if match < SEL:
                    if populations.iloc[selGeneNum[0]].at['fitness'] < populations.iloc[selGeneNum[1]].at['fitness']:
                        parents_index[i] = selGeneNum[0]
                    else:
                        parents_index[i] = selGeneNum[1]
                else:
                    if populations.iloc[selGeneNum[0]].at['fitness'] < populations.iloc[selGeneNum[1]].at['fitness']:
                        parents_index[i] = selGeneNum[1]
                    else:
                        parents_index[i] = selGeneNum[0]
            # crossover : order-based crossover
            daddy_value = populations.iloc[parents_index[0]].at['chromosome'].copy()
            mommy_value = populations.iloc[parents_index[1]].at['chromosome'].copy()
            CsGeneNum = randomTwo(cities_count)
            offspring = daddy_value[CsGeneNum[0]: CsGeneNum[1]]
            for i in daddy_value[CsGeneNum[0]: CsGeneNum[1]]:
                mommy_value.remove(i)
            for i in range(len(offspring)):
                mommy_value.insert(CsGeneNum[0] + i, offspring[i])
            offspring = mommy_value
            offspring_fit = cal_fit(offspring)

            # print(endGen, '번째 crossover 결과(미정렬) : \n', populations)
            # mutation : exchange mutation
            mut_p = random.random()
            if mut_p < MUT:
                MtGeneNum = randomTwo(cities_count)
                mut_Temp = offspring[MtGeneNum[0]]
                offspring[MtGeneNum[0]] = offspring[MtGeneNum[1]]
                offspring[MtGeneNum[1]] = mut_Temp
                offspring_fit = cal_fit(offspring)
            populations = populations.append({'chromosome' : offspring, 'fitness' : offspring_fit}, ignore_index=True)
        # Replacement
        populations.sort_values(by=['fitness'], inplace=True)
        populations.reset_index(drop=True, inplace=True)
        populations.drop(populations.index[50:74], inplace=True)
        print(generation, '번째 연산 결과 : \n', populations.loc[0], len(populations))

@timeout(limit_time)
def start_GA(stri) :
    make_distDataframe(stri)
    TSP_GA()

try :
    start = timeit.default_timer()
    start_GA("2opt_dots/2opt_cycle100.in")
    stop = timeit.default_timer()
    print(stop - start)
except :
    stop = timeit.default_timer()
    print(stop - start)
