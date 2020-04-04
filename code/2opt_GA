import math
import timeit
import numpy as np
# import pandas as pd
import random

dist_ar = [] # 거리표(global)
limit_time = 0 # 제한시간(global)
cities_count = 0 # 도시 수(global)
dots_list = [] # 도시 리스트(global)

# Hyper Parameter
MUT = 0.2 # 변이확률
SEL = 0.85 # 선택압
END = 1000 # 최종세대 설정
chrCOUNT = 50 # 해집단 내 염색체 개수
selCOUNT = 25 # selection시 선택되는 상위 염색체의 개수

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
    for i in range(len(stri)-1) :
        fit += dist_ar[stri[i], stri[i+1]]
    return fit

# 2opt-algo function
def optFunc(stri) :
    head = random.randrange(1, len(stri)-2)
    tail = random.randrange(head, len(stri)-1)
    newArr = []

    # str[0] - str[head-1] 까지 순서대로 나열
    for i in range(head) :
        newArr.append(stri[i])

    # str[head] - str[tail] 까지 역순 나열
    for i in range(len(stri[head-1:tail])) :
        newArr.append(stri[tail-i])

    # str[head+1] - str[-1] 까지 순서대로 나열
    for i in range(len(stri)-tail-1) :
        newArr.append(stri[tail+i+1])

    return newArr

def TSP_GA() :
    # 환경 설정 및 초기화
    generation = 1  # 현재 세대
    population = [] # 현재 세대 or initializing시 최종 population
    population_fit = [] # population의 적합도
    populations = [] #population과 적합도로 이루어진 이차원 배열
    step_result = [] # step을 거칠 때 변화된 population

    # initialize
    for i in range(chrCOUNT) :
        population.append(optFunc(random.sample(range(0, cities_count), cities_count)))

    for i in range(chrCOUNT) :
        population_fit.append(round(cal_fit(population[i]), 5))

    populations = np.array([population, population_fit])
    populations = populations.T
    # print('초기 염색체 : \n', population, '\n염색체 별 적합도 :\n', population_fit)
    # print(populations)

    for endGen in range(END) :
        # selection : 토너먼트선택,
        populations = populations[np.argsort(populations[:, 1])]
        # print(endGen, '번째 selection 결과 : \n', populations)
        for endSel in range(selCOUNT) :
            # 난수룰 발생시켜 해집단 내 두 유전자 선택, 선택난수 발생
            # 선택난수가 선택압보다 작으면 두 유전자 중 좋은 유전자가 살아남음. 아니면 반대로
            parents_index = [0]*2
            for i in range(len(parents_index)):
                firGeneNum = random.randrange(0, chrCOUNT - endSel - 1)
                secGeneNum = random.randrange(firGeneNum + 1, chrCOUNT - endSel)
                match = random.random()
                if match < SEL :
                    if populations[firGeneNum,1] < populations[secGeneNum,1] :
                        parents_index[i] = firGeneNum
                    else:
                        parents_index[i] = secGeneNum
                else:
                    if populations[firGeneNum,1] < populations[secGeneNum,1] :
                        parents_index[i] = secGeneNum
                    else:
                        parents_index[i] = firGeneNum
            # crossover : order-based crossover
            daddy_value = populations[parents_index[0], 0].copy()
            mommy_value = populations[parents_index[1], 0].copy()
            headCSLine = random.randrange(0, cities_count-1)
            tailCSLine = random.randrange(headCSLine+1, cities_count)
            offspring = daddy_value[headCSLine: tailCSLine]
            for i in daddy_value[headCSLine : tailCSLine] :
                mommy_value.remove(i)
            for i in range(len(offspring)) :
                mommy_value.insert(headCSLine+i, offspring[i])
            offspring = optFunc(mommy_value)
            offspring_fit = cal_fit(offspring)

            # print(endGen, '번째 crossover 결과(미정렬) : \n', populations)
            # mutation : exchange mutation
            mut_p = random.random()
            if mut_p < MUT :
                headPoint = random.randrange(0, cities_count-1)
                tailPoint = random.randrange(headPoint+1, cities_count)
                mut_Temp = offspring[headPoint]
                offspring[headPoint] = offspring[tailPoint]
                offspring[tailPoint] = mut_Temp
                offspring_fit = cal_fit(offspring)
            populations = np.vstack((populations, [offspring, offspring_fit]))
        # Replacement
        populations = populations[np.argsort(populations[:, 1])]
        for i in range(25) :
            np.delete(populations, (50+i), axis=0)
        print(endGen, '번째 연산 결과 : \n', populations[0,0],"\n", populations[0,1])

# start
# select_pob = str(input("문제파일의 이름을 포함한 경로를 입력해주세요.\nex) dots/cycle21.in\n"))
# print(select_pob)
start = timeit.default_timer()
make_distDataframe("dots/cycle318.in")
TSP_GA()
stop = timeit.default_timer()
print(stop-start)
