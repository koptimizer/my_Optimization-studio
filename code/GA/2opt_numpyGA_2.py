import math
import numpy as np
import random
import timeit
from threading import Thread
import functools

dist_ar = [] # 거리표(global)
# limit_time = 36 # 제한시간(global)
cities_count = 0 # 도시 수(global)
dots_list = [] # 도시 리스트(global)

# Hyper Parameter
limits = (60) * 36 # 제한시간
MUT = 0.2 # 변이확률
SEL = 0.85 # 선택압
chrCOUNT = 50 # 해집단 내 염색체 개수
selCOUNT = 25 # selection시 선택되는 상위 염색체의 개수

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

# 거리표 제작(param : 문제 경로) : dist_df
def make_distDataframe(str):
    global dist_ar
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

    dist_ar = np.array(dist_ar)
    print(dist_ar)

# 거리표를 이용한 적합도 매칭 함수
def cal_fit(stri) :
    fit = 0
    for steps in range(len(stri)-1) :
        fit += dist_ar[stri[steps], stri[steps+1]]
    return fit

# 2opt-algorithm
def optFunc(stri) :
    head = random.randrange(1, len(stri)-2)
    tail = random.randrange(head+1, len(stri)-1)
    newArr = []

    # str[0] - str[head-1] 까지 순서대로 나열
    for spot1 in range(head) :
        newArr.append(stri[spot1])

    # str[head] - str[tail] 까지 역순 나열
    for spot2 in range(len(stri[head-1:tail])) :
        newArr.append(stri[tail-spot2])

    # str[head+1] - str[-1] 까지 순서대로 나열
    for spot3 in range(len(stri)-tail-1) :
        newArr.append(stri[tail+spot3+1])

    return newArr

# 0 ~ ranges-1의 범위 중 두 개를 랜덤으로 샘플링해서 list 리턴
def randomTwo(ranges) :
    randomList = []
    randomList += random.sample(range(0,ranges), 2)
    randomList.sort()
    return randomList

def TSP_GA() :
    # 환경 설정 및 초기화
    generation = 0  # 현재 세대
    chromosome = [] # temp chromosome
    chromosome_fit = [] # temp fitness

    # initialize
    for i in range(chrCOUNT) :
        # 2opt 이용해서 좀 더 좋은 initial chromosome 설정
        chromosome.append(optFunc(random.sample(range(0, cities_count), cities_count)))

    for i in range(chrCOUNT) :
        chromosome_fit.append(round(cal_fit(chromosome[i]), 5))

    populations = np.array([chromosome, chromosome_fit])
    populations = populations.T
    # print('초기 염색체 : \n', population, '\n염색체 별 적합도 :\n', population_fit)
    # print(populations)

    while 1 :
        generation+=1
        populations = populations[np.argsort(populations[:, 1])]
        # 최적화 알고리즘 2-opt 사용
        for i in range(selCOUNT) :
            populations[i+selCOUNT,0] = optFunc(populations[i+selCOUNT,0])
            populations[i+selCOUNT,1] = cal_fit(populations[i+selCOUNT,0])

        # selection : 토너먼트선택,
        populations = populations[np.argsort(populations[:, 1])]
        for endSel in range(selCOUNT) :
            # 난수룰 발생시켜 해집단 내 두 유전자 선택, 선택난수 발생
            # 선택난수가 선택압보다 작으면 두 유전자 중 좋은 유전자가 선택. 아니면 반대로
            parents_index = [0]*2
            for i in range(len(parents_index)):
                selGeneNum = randomTwo((chrCOUNT-endSel))
                match = random.random()
                if match < SEL :
                   if populations[selGeneNum[0],1] < populations[selGeneNum[1],1] :
                        parents_index[i] = selGeneNum[0]
                   else:
                        parents_index[i] = selGeneNum[1]
                else :
                    if populations[selGeneNum[0],1] < populations[selGeneNum[1],1] :
                        parents_index[i] = selGeneNum[1]
                    else:
                        parents_index[i] = selGeneNum[0]
            # crossover : order-based crossover
            daddy_value = populations[parents_index[0], 0].copy()
            mommy_value = populations[parents_index[1], 0].copy()
            CsGeneNum = randomTwo(cities_count)
            offspring = daddy_value[CsGeneNum[0] : CsGeneNum[1]]
            for i in daddy_value[CsGeneNum[0] : CsGeneNum[1]] :
                mommy_value.remove(i)
            for i in range(len(offspring)) :
                mommy_value.insert(CsGeneNum[0]+i, offspring[i])
            offspring = mommy_value
            offspring_fit = cal_fit(offspring)

            # mutation : exchange mutation
            mut_p = random.random()
            if mut_p < MUT :
                MtGeneNum = randomTwo(cities_count)
                mut_Temp = offspring[MtGeneNum[0]]
                offspring[MtGeneNum[0]] = offspring[MtGeneNum[1]]
                offspring[MtGeneNum[1]] = mut_Temp
                offspring_fit = cal_fit(offspring)
            populations = np.vstack((populations, [offspring, offspring_fit]))
        # Replacement
        populations = populations[np.argsort(populations[:, 1])]
        for i in range(chrCOUNT-selCOUNT) :
            np.delete(populations, (chrCOUNT+i), axis=0)
        print(generation, '세대 최적 해 : \n', populations[0,0],"\n", populations[0,1])

@timeout(limits)
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


'''
//질문
1. 36초만에 200,000세대까지 계산하는건 어려운 일(*GA_2차보고서) 같은데... 36분이 아닌지...?
2. population 전체에 2opt를 실행하니 오히려 수렴을 못하는 결과 발생... 
    하위 *selCount개의 chromosome에 2opt를 시행했더니 결과가 훨씬 좋았음.
    2opt를 거친다고해서 fitness가 무조건 좋아지는 것은 아닌것은 알겠는데 어떻게 적용해야 가장 최적일까???
    ex) 하위 몇 %만 적용, 적용과 미적용을 비교해서 좋은 경우만 대치

//이슈
1. python에서 thread로 함수를 중간에 죽이는게 windows에서 일반적으로 불가. 삽질 너무 많이 했음...ㅠ
    데코레이터(?)를 만들고 Thread.join (timeout) 메서드를 사용. 
    죽이는 것은 아니라서 백그라운드에서 실행 유지.
2. 특정 범위 내의 중복되지 않는 두 개의 랜덤을 골라내는 것에도 삽질 많이함.
3. 코드를 좀 수정해서 모듈화를 진행했으나 교수님이 지도해주시기엔 좋지 못한 것 같아서 다시 합침... 

//비교
optGA : numpy + 2-opt GA
numGA : numpy GA
panGA : pandas GA
시간제한 : 36s
타겟 : 2opt_cycle100.in

panGA : generation / fitness
    356/2272
    375/2349
    381/2218
    348/2553
    381/2467
    
numGA : generation / fitness
    1171/1836
    1159/2005
    1175/1812
    1174/1947
    1131/1931
    
optGA : generation / fitness
    1141/1182
    1142/1136
    1126/1205
    1128/1214
    1142/1219
'''
