# GA 연습 1
# 0부터 1024-1까지 가장 큰 수를 GA로 찾는 과정과 결과를 보여주는 것이 목표
# 탐색결과 해집단의 해들이 일정 비율 동일하면, 최적 해로 수렴했다고 보고 탐색을 종료(세대 수 반환)
import random as rand

# -----수정 가능한 파라미터-----
MUT = 5 # 변이확률(%)
END = 90 # 탐색을 끝낼지 결정해주는 population내 수렴한 chromosome의 비율(%)
CMSCOUNT = 100 # population내 chromosome 수
selection_values = 50 # selection시 적합도 순위 결정수, CMSCOUNT에 가까울수록 선택압 낮아짐
# ----------------------------

def GA():
	ranges = 1024 # 탐색 범위
	generation = 0 # 세대 수
	population = [] # 해당 세대 결과 population
	step_result = [] # 해당 세대 각 단계별 population
	#intialize
	initials = []
	for i in range(CMSCOUNT) :
		# 자릿수가 맞춰지지가 않아서 zfill로 피팅
		initial_values = bin(rand.randrange(0,ranges)).replace('0b','').zfill(10)
		initials.append(initial_values)
	population = initials[:]
	print("initialzed population : \n", population, "\n\n")

	while 1 :
		generation += 1
		result = population[:]

		#selection (순위기반선택)
		selections = []
		result.sort(reverse=True) # stable sort
		for i in range(selection_values) :
			selections.append(result[i])

		result = selections[:]
		selctions = []
		print(generation,"st selections : \n",result)

		# crossover (순위기반선택으로 추출된 유전자를 이용해 자식 유전자 생성)
		crossovers = []
		for i in range(len(result)) :
			crossovers.append(result[i]) # selected 부모 유전자

		baby_values = ""
		# 설정한 전체 유전자 수 - selected 부모 유전자 수 만큼 자식 유전자 수 생성 
		for i in range(CMSCOUNT-len(crossovers)) :
			daddy = rand.randrange(0,selection_values)
			mommy = rand.randrange(0,selection_values)
			daddy_values = result[daddy]
			mommy_values = result[mommy]
			for u in range(len(daddy_values)) :
				n = daddy_values[u]
				m = mommy_values[u]
				if n == m :
					baby_values += n
				if n != m :
					who = rand.randrange(0,2)
					if who == 0 :
						baby_values +=n
					elif who == 1 :
						baby_values +=m
			crossovers.append(baby_values) 
			baby_values = ""
		# crossovers.sort(reverse=True)

		result = crossovers[:]
		crossovers = []
		print(generation,"st crossover : \n",result)

		#mutation (MUT에 설정된 확률을 result[50 : 100]인 자식 유전자들에 적용)
		mutations = result[:]
		for i in range(len(result)-50) :
			mutava = rand.randrange(1,101)
			if mutava > MUT :
				pass
			elif mutava <= MUT :
				mutations[i+50] = bin(rand.randrange(0,ranges)).replace('0b','').zfill(10)
		mutations.sort(reverse=True)

		result = mutations[:]
		mutations = []
		print(generation,"st mutation : \n", result)

		# replace (해당 세대의 population을 GA를 거친 염색체 집합으로 대체)
		population = result[:]
		print(generation,"st population :\n", population, "\n\n")
		
		# evaluate
		# population내 chromosome들의 END만큼이 같은 chromosome으로 수렴했다면 
		# 탐색을 멈추고 수렴한 chromosome의 값과 세대 수 반환
		bestJudge = int(CMSCOUNT*(END/100))
		if population[0] == population[bestJudge] :
			bestValues = int("0b"+population[0],2)
			print("---------------탐색 완료---------------\n최종 값 :",bestValues,"\n세대 수 : ",generation)
			break
		else :
			pass

GA()
	

