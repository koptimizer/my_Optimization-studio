import numpy as np
import math
import pandas as pd
import random

pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)

dist_df = [] # 거리표(global)
limit_time = 0 # 제한시간(global)
cities_count = 0 # 도시 수(global)
dots_list = [] # 도시 리스트(global)

# Hyper Parameter
MUT = 0.25 # 변이확률
SEL = 0.8 # 선택압
END = 1 # 최종세대 설정
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

def TSP_GA() :
    # 환경 설정 및 초기화
    generation = 1  # 현재 세대
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
    print('초기 염색체 : \n', population, '\n염색체 별 적합도 :\n', population_fit)
    for endGen in range(END) :
        # selection : 토너먼트선택,
        for endSel in range(selCOUNT) :
            # 난수룰 발생시켜 해집단 내 두 유전자 선택, 선택난수 발생
            firGeneNum = random.randrange(0, chrCOUNT-endSel)
            secGeneNum = random.randrange(0, chrCOUNT-endSel)
            match = random.random()
            # 선택난수보다 선택압이 작으면 두 유전자 중 큰 유전자가 살아남음. 아니면 반대로
            if match < SEL :
                if populations.iloc[firGeneNum].at['fitness'] >= populations.iloc[secGeneNum].at['fitness'] :
                    populations.drop([populations.index[secGeneNum]], inplace = True)
                else :
                    populations.drop([populations.index[firGeneNum]], inplace = True)
            else :
                if populations.iloc[firGeneNum].at['fitness'] >= populations.iloc[secGeneNum].at['fitness'] :
                    populations.drop([populations.index[firGeneNum]], inplace = True)
                else:
                    populations.drop([populations.index[secGeneNum]], inplace= True)
        populations.sort_values(by=['fitness'], ascending = False, inplace = True)
        print(endGen, '번째 selection 결과 : \n', populations)

        # crossover : order-based crossover(oxc)
        #for i in range(selCOUNT) :
            # daddy_value = populations.at(random.randrange(0,selCOUNT),'chromosome')
            # mommy_index = populations.at(random.randrange(0,selCOUNT),'chromosome')
            # headCSLine = random.randrange(0, cities_count-1)
            # tailCSLine = random.randrange(headCSLine, cities_count)

        # mutation : exchange mutation









# start
# select_pob = str(input("문제파일의 이름을 포함한 경로를 입력해주세요."))
# make_distDataframe(select_pob)
# TSP_GA()

make_distDataframe('./dots/cycle.in')
TSP_GA()

