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
MUT = 0.2 # 변이확률
SEL = 0.85 # 선택압
END = 500 # 최종세대 설정
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
    print(populations)
    for endGen in range(END) :
        # selection : 토너먼트선택,
        for endSel in range(selCOUNT) :
            # 난수룰 발생시켜 해집단 내 두 유전자 선택, 선택난수 발생
            firGeneNum = random.randrange(0, chrCOUNT-endSel-1)
            secGeneNum = random.randrange(firGeneNum+1, chrCOUNT-endSel)
            match = random.random()
            # 선택난수가 선택압보다 작으면 두 유전자 중 좋은 유전자가 살아남음. 아니면 반대로
            if match < SEL :
                if populations.iloc[firGeneNum].at['fitness'] < populations.iloc[secGeneNum].at['fitness'] :
                    populations.drop([populations.index[secGeneNum]], inplace = True)
                else :
                    populations.drop([populations.index[firGeneNum]], inplace = True)
            else :
                if populations.iloc[firGeneNum].at['fitness'] < populations.iloc[secGeneNum].at['fitness'] :
                    populations.drop([populations.index[firGeneNum]], inplace = True)
                else:
                    populations.drop([populations.index[secGeneNum]], inplace= True)
        populations.sort_values(by=['fitness'], inplace = True)
        populations.reset_index(drop = True, inplace = True)
        print(endGen, '번째 selection 결과 : \n', populations)

        # crossover : order-based crossover
        for i in range(selCOUNT) :
            daddy_count = random.randrange(0,selCOUNT-1)
            mommy_count = random.randrange(daddy_count+1, selCOUNT)
            daddy_value = populations.iloc[daddy_count].at['chromosome'].copy()
            mommy_value = populations.iloc[mommy_count].at['chromosome'].copy()
            headCSLine = random.randrange(0, cities_count-1)
            tailCSLine = random.randrange(headCSLine+1, cities_count)
            offspring = daddy_value[headCSLine : tailCSLine]
            for i in daddy_value[headCSLine : tailCSLine] :
                if i in mommy_value :
                    mommy_value.remove(i)
            for i in range(len(offspring)) :
                mommy_value.insert(headCSLine+i, offspring[i])
            offspring = mommy_value
            offspring_fit = cal_fit(offspring)
            populations = populations.append({'chromosome' : offspring, 'fitness' : offspring_fit}, ignore_index=True)
        print(endGen, '번째 crossover 결과(미정렬) : \n', populations)

        # mutation : exchange mutation
        for i in range(selCOUNT) :
            mut_p = random.random()
            if mut_p < MUT :
                mut_value = populations.iloc[i + 25].at['chromosome']
                headPoint = random.randrange(0, cities_count-1)
                tailPoint = random.randrange(headPoint+1, cities_count)
                mut_Temp = mut_value[headPoint]
                mut_value[headPoint] = mut_value[tailPoint]
                mut_value[tailPoint] = mut_Temp
                mut_fit = cal_fit(mut_value)
                populations.loc[i + 25]['chromosome'] = mut_value
                populations.loc[i + 25]['fitness'] = mut_fit
            else :
                pass
        populations.sort_values(by=['fitness'], inplace = True)
        populations.reset_index(drop=True, inplace=True)

        print(endGen, '번째 mutation 및 정렬 결과 : \n', populations)

# start
select_pob = str(input("문제파일의 이름을 포함한 경로를 입력해주세요."))
print("ex) ./dots/cycle21.in")
make_distDataframe(select_pob)
TSP_GA()
