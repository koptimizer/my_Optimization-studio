import math
import numpy as np
import random

# 적합도 산출 함수
def cal_fit(stri) :
    fit = 0
    if stri == ["0", "1", "0", "1", "0", "0"] :
        fit += 9999
    elif stri[-1] == "0" :
        fit += -1
    else :
        fit += 1
    return fit

# 0 ~ ranges-1의 범위 중 두 개를 랜덤으로 샘플링해서 list 리턴
def randomTwo(ranges) :
    randomList = []
    randomList += random.sample(range(0,ranges), 2)
    randomList.sort()
    return randomList

# 랜덤한 chromosome 생성
def makeChr() :
    temp = []
    for j in range(1,7) :
        temp += str(random.sample(range(0, 2), 1)[0])
    return temp

def TSP_GA() :
    global buffer
    # 환경 설정 및 초기화
    generation = 1  # 현재 세대
    population = [] # 현재 세대 or initializing시 최종 population
    population_fit = [] # population의 적합도

    # initialize
    for i in range(chrCOUNT) :
        population.append(makeChr())

    for i in range(chrCOUNT) :
        population_fit.append(cal_fit(population[i]))

    populations = np.array([population, population_fit])
    populations = populations.T

    for i in range(END):
        generation += 1
        populations = populations[np.argsort(populations[:, 1])]

        # selection : 토너먼트선택,
        populations = populations[np.argsort(populations[:, 1])]
        for endSel in range(selCOUNT):
            # 난수룰 발생시켜 해집단 내 두 유전자 선택, 선택난수 발생
            # 선택난수가 선택압보다 작으면 두 유전자 중 좋은 유전자가 선택. 아니면 반대로
            parents_index = [0] * 2
            for i in range(len(parents_index)):
                selGeneNum = randomTwo((chrCOUNT - endSel))
                match = random.random()
                if match < SEL:
                    if populations[selGeneNum[0], 1] < populations[selGeneNum[1], 1]:
                        parents_index[i] = selGeneNum[0]
                    else:
                        parents_index[i] = selGeneNum[1]
                else:
                    if populations[selGeneNum[0], 1] < populations[selGeneNum[1], 1]:
                        parents_index[i] = selGeneNum[1]
                    else:
                        parents_index[i] = selGeneNum[0]
            # crossover : order-based crossover
            daddy_value = populations[parents_index[0], 0].copy()
            mommy_value = populations[parents_index[1], 0].copy()
            CsGeneNum = randomTwo(state_count)
            offspring = daddy_value[CsGeneNum[0]: CsGeneNum[1]]
            del mommy_value[CsGeneNum[0]: CsGeneNum[1]]
            for i in range(len(offspring)):
                mommy_value.insert(CsGeneNum[0] + i, offspring[i])
            offspring = mommy_value
            offspring_fit = cal_fit(offspring)

            # mutation : exchange mutation
            mut_p = random.random()
            if mut_p < MUT:
                MtGeneNum = randomTwo(state_count)
                mut_Temp = offspring[MtGeneNum[0]]
                offspring[MtGeneNum[0]] = offspring[MtGeneNum[1]]
                offspring[MtGeneNum[1]] = mut_Temp
                offspring_fit = cal_fit(offspring)
            populations = np.vstack((populations, [offspring, offspring_fit]))
        # Replacement
        populations = populations[np.argsort(-populations[:, 1])]
        for i in range(chrCOUNT - selCOUNT):
            np.delete(populations, (chrCOUNT + i), axis=0)
        if generation % 5 == 0 :
            print(generation, '세대 최적 해 : \n', populations[0, 0], "\n", populations[0, 1])
        # 수렴 확인
        if generation % 307 == 0 :
            buffer = populations[0,0]
        if generation % 997 == 0:
            if buffer == populations[0,0] :
                print("수렴했습니다.")
                break

if __name__ == "__main__" :
    state_count = 6  # 상태 수

    # Hyper Parameter
    MUT = 0.2  # 변이확률
    SEL = 0.85  # 선택압
    END = 10000  # 최종세대 설정
    chrCOUNT = 20  # 해집단 내 염색체 개수
    selCOUNT = 10  # selection시 선택되는 상위 염색체의 개수

    # 수렴했는지 확인시켜줄 버퍼
    buffer = 0

    TSP_GA()