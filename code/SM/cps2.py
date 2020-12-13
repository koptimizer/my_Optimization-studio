import numpy as np
import random as rd
import math as mt

rd.seed(777)

class Machine :
    # ['Set', job, operation, machine, processingTime, start]
    def __init__(self, setup, number):
        # print('...'+str(number)+'번 Machine를 초기화중입니다...')
        self.isIdle = True
        self.setup = setup
        self.number = number
        self.machine_time = 0
        self.recentSetup = 0
        self.queue = [] # 아직 못들어간 대기 엔티티들
        self.system = [] # 기계 안에서 직접 할당중인 엔티티

    def allocation(self, info):
        self.system.append(info)
        self.isIdle = False
        self.recentSetup = int(info[0])
        return info

    def deallocation(self):
        self.system.pop()
        self.isIdle = True

class Simulator :
    def __init__(self, environment, setup, number_of_jobs, operations_per_jobs, number_of_machines):
        print('...Simulator를 초기화중입니다...')
        self.environment = environment
        self.number_of_jobs = number_of_jobs
        self.operations_per_jobs = operations_per_jobs
        self.number_of_machines = number_of_machines
        self.setup = setup

        self.machineInit()

        self.eventlist = []
        self.TNOW = 0
        self.index = 0
        self.completer = []
        print('Simulating 준비가 모두 끝났습니다.')

    def initialize(self):
        self.eventlist = []
        self.TNOW = 0
        self.index = 0
        self.completer = []
        self.machineInit()

    def machineInit(self):
        self.machineList = []
        self.machine_assign = []
        self.machine_per_index = []
        for i in range(1, self. number_of_machines+1) :
            self.machineList.append(Machine(self.setup[i-1], i))
            self.machine_assign.append([])
            self.machine_per_index.append(0)

    def sortEventlist(self):
        self.eventlist = sorted(self.eventlist, key=lambda x : x[-1])

    def feasibleChecker(self):
        # TODO Fully Feasible 체커는 좀 나중에 구현하는 걸로... 방법은 J,O 떼와서 정렬인지 확인 + M할당 적합성 확인?
        return True

    def getDepartureInfo(self, JOM):
        alloc_machine = self.machineList[int(JOM[2]) - 1]
        job = int(JOM[0])
        operation = int(JOM[1])
        machine = int(JOM[2])
        processingTime = self.environment[job-1][operation-1][machine-1]

        if alloc_machine.recentSetup == 0 :
            processingTime += self.setup[int(job)-1][int(job)-1]  # 디폴트 셋업
        elif alloc_machine.recentSetup != job or alloc_machine.recentSetup != int(job) :
            processingTime += self.setup[int(job)-1][alloc_machine.recentSetup - 1]

        finishTime = self.TNOW + processingTime

        alloc_machine.allocation([job, operation, machine, processingTime, finishTime])

        return ['Dep', job, operation, machine, processingTime, finishTime]

    def output_per_index(self):
        print(self.index, "번 째 Event list :", self.eventlist, 'TNOW : ', self.TNOW)

    def machine_assigner(self):
        for i in self.solution :
            self.machine_assign[int(i[2])-1].append(i)

    def finder(self, JO):
        finder = None
        for i in range(self.number_of_machines) :
            try :
                if JO == str(int(self.machine_assign[i][self.machine_per_index[i]][0:2])-1) and self.machineList[i].isIdle == True :
                    finder = self.machine_assign[i][self.machine_per_index[i]]
            except :
                pass

        return finder

    def simulate(self, solution):
        self.initialize()
        self.solution = solution
        if self.feasibleChecker() == False : # 모든 해가 유효하게 가정 및 유도
            print("해가 유효하지 않습니다.")
            return

        # print(solution)
        self.machine_assigner() # Machine assign 산출
        # print(self.machine_assign)
        for i in range(self.number_of_machines) :
            try :
                if self.machine_assign[i][0][1] == '1' :
                    todo = self.machine_assign[i][0]
                    self.eventlist.append(self.getDepartureInfo(todo))
            except :
                pass

        self.eventlist.append(['End', 9999, 9999, 9999, 9999, 9999])
        self.sortEventlist()
        # self.output_per_index()

        while self.eventlist[0][0] != 'End' :
            self.index += 1 # 인덱스 +1
            # self.output_per_index()
            self.TNOW = self.eventlist[0][-1]
            currenter = self.machine_assign[int(self.eventlist[0][3]) - 1][self.machine_per_index[int(self.eventlist[0][3]) - 1]]  # JOM
            self.machineList[int(self.eventlist[0][3])-1].deallocation()
            self.completer.append(currenter[0:2])  # JO
            self.eventlist.pop(0)
            # print(currenter, '를 해치웠다!', self.TNOW)
            # print("case0")

            # JOM 다음이 JO+1M일경우 바로 할당
            try :
                nexter = self.machine_assign[int(currenter[-1])-1][self.machine_per_index[int(currenter[-1])-1]+1] # J'O'M'
                if currenter == str(int(nexter) - 10):
                    todo = nexter
                    self.eventlist.append(self.getDepartureInfo(todo))
                    # print("case1-1")

                # JOM 다음이 J'O'M인데, J', O'-1이 끝난 상황이면 바로 할당
                elif (str(int(nexter[0:2]) - 1) in self.completer or nexter[1] == '1') and currenter[-1] == nexter[-1] and currenter != nexter:
                    todo = nexter
                    self.eventlist.append(self.getDepartureInfo(todo))
                    # print("case2-1")

                elif nexter[1:3] == currenter[1:3] and nexter[1] == '1' :
                    todo = nexter
                    self.eventlist.append(self.getDepartureInfo(todo))
                    # print("case3-1")
            except :
                pass

            finder = self.finder(currenter[0:2])
            if finder != None :
                todo = finder
                self.eventlist.append(self.getDepartureInfo(todo))
                # print("case4-1")


            self.sortEventlist()
            if self.machine_per_index[int(currenter[2])-1] < len(self.machine_assign[int(currenter[2])-1]) :
                self.machine_per_index[int(currenter[2])-1] +=1

        # self.output_per_index()
        return self.TNOW

class CuckooSearch :
    def __init__(self, popSize, maxIter, number_of_jobs, operations_per_jobs, number_of_machines, target_env, method, output_per_iter):
        self.number_of_jobs = number_of_jobs
        self.operation_per_jobs = operations_per_jobs
        self.number_of_machines = number_of_machines
        self.target_env = target_env
        self.popSize = popSize
        self.maxIter = maxIter
        self.pa = 0.25
        self.selPres = 0.5
        self.iteration = 0
        self.population = []
        self.method = method
        self.output_per_iter = output_per_iter

    def initialize(self):
        solution = []
        env = []
        for i in range(1, self.number_of_jobs+1) :
            jobNum = i
            temp = []
            for j in range(1, self.operation_per_jobs+1) :
                temp.append(str(jobNum)+str(j))
            env.append(temp)

        while 1 :
            if env == [[], [], [], []] :
                break
            rand1 = rd.randint(0, self.number_of_jobs-1)
            try :
                solution.append(env[rand1].pop(0))
            except :
                pass

        solution_result = []
        for i in solution :
            machine = 0
            job = i[0]
            operation = i[1]
            machine_pool = self.target_env[int(job)-1][int(operation)-1]
            while 1:
                rand2 = rd.randint(1, len(machine_pool))
                if np.isnan(self.target_env[int(job)-1][int(operation)-1][rand2-1]) :
                    pass
                else :
                    machine = rand2
                    break
            solution_result.append(i+str(machine))

        return solution_result

    def get_fitness(self, solution):
        return self.method.simulate(solution)

    def sorting(self):
        self.population = sorted(self.population, key=lambda x : x[-1])

    def levyFlight(self):
        return mt.pow(rd.uniform(0.0001, 0.9999), -1.0 / 3.0)

    def largeStep(self, solution):
        return self.initialize()

    def smallStep(self, solution):
        new_solution = []
        for i in range(self.popSize) :
            if rd.random() >= 0.5 :
                currenter = solution[i]
                currenter1 = currenter[0]
                currenter2 = currenter[1]
                currenter3 = currenter[2]
                newer = currenter1 + currenter2
                machine_pool = self.target_env[int(currenter1)-1][int(currenter2)-1]
                while 1:
                    rand1 = rd.randint(1, len(machine_pool))
                    if np.isnan(self.target_env[int(currenter1)-1][int(currenter2)-1][rand1-1]) or rand1 == int(currenter3) :
                        pass
                    else :
                        newer += str(rand1)
                        break
                new_solution.append(newer)
            else :
                new_solution.append(solution[i])

        return new_solution

    def search(self):
        # initialize
        for i in range(self.popSize) :
            temp = []
            temp.append(self.initialize())
            temp.append(self.get_fitness(temp[0]))
            self.population.append(temp)
        self.sorting()

        print(self.population)

        for iter in range(self.maxIter) :
            self.iteration += 1

            # Get a randomly cuckoo's step by levy flight
            hostNest_ref = rd.randint(0, int(self.selPres * self.popSize))
            hostNest = self.population[hostNest_ref]
            cuckooNest = []

            if self.levyFlight() > 2:
                cuckooNest.append(self.largeStep(hostNest[0]))
            else :
                cuckooNest.append(self.smallStep(hostNest[0]))

            cuckooNest.append(self.get_fitness(cuckooNest[0]))

            if hostNest[1] > cuckooNest[1] :
                self.population[hostNest_ref] = cuckooNest
            self.sorting()

            for i in range(self.popSize - int(self.pa * self.popSize), self.popSize) :
                temp = []
                temp.append(self.initialize())
                temp.append(self.get_fitness(temp[0]))
                self.population[i] = temp
            if self.iteration % self.output_per_iter == 0 :
                print(self.iteration, "번 째 최적 해 : \n", self.population[0])
            self.sorting()

if __name__ == "__main__" :
    target_env = [
        [[20, 15, 18, 17], [7, np.nan, 8, np.nan], [12, 10, np.nan, 15], [14, np.nan, 12, 12], [11, np.nan, 12, 12]],
        [[np.nan, 23, np.nan, 32], [22, np.nan, 12, np.nan], [23, 19, np.nan, np.nan], [27, np.nan, np.nan, 25], [np.nan, 13, 16, np.nan]],
        [[16, 5, 5, 4], [np.nan, 5, np.nan, 5], [12, 5, 5, 7], [np.nan, 5, np.nan, 5], [14, 5, 6, 7]],
        [[12, np.nan, 14 ,np.nan], [17, np.nan, 18, np.nan], [np.nan, 20, np.nan, 21], [22, np.nan ,np.nan, 23], [np.nan, 12, 26, np.nan]],
    ]

    setup_time = [[5, 4, 2, 4],
                  [2, 5, 2, 3],
                  [1, 5, 5, 1],
                  [4, 4, 4, 5]]

    number_of_jobs = 4
    operations_per_jobs = 5
    number_of_machines = 4

    pang_solution = ['111', '212', '314', '413', '121',
                '223', '322', '423', '131', '232',
                '333', '434', '143', '241', '342',
                '444', '154', '253', '352', '452']

    minju_solution = ['314', '212', '411', '113', '324',
                      '223', '121', '423', '333', '232',
                      '131', '434', '143', '244', '441',
                      '342', '352', '452', '253', '151']

    minju_solution2 = ['212', '114', '313', '411', '223',
                       '421', '121', '322', '132', '232',
                       '434', '333', '444', '342', '241',
                       '143', '153', '252', '353', '453']

    fuck_solution = ['311', '111', '121', '134', '413',
                     '214', '223', '423', '144', '154',
                     '232', '241', '253', '432', '324',
                     '331', '441', '452', '342', '352']

    ins1 = ['214', '413', '423', '311', '324',
            '332', '434', '342', '444', '452',
            '113', '121', '134', '351', '223',
            '231', '144', '241', '154', '253']

    ins2 = ['212', '413', '421', '313', '322',
            '332', '434', '344', '441', '453',
            '112', '123', '134', '351', '223',
            '232', '144', '244', '154', '253']

    cuckoo0 = ['111', '413', '212', '121', '134',
               '143', '223', '313', '322', '154',
               '421', '432', '444', '333', '231',
               '241', '253', '452', '342', '351']

    cuckoo1 = ['411', '421', '434', '212', '313',
               '113', '322', '223', '121', '131',
               '444', '232', '334', '452', '344',
               '354', '241', '143', '151', '253']

    cuckoo2 = ['411', '114', '212', '313', '421',
               '324', '121', '223', '434', '333',
               '131', '232', '344', '143', '352',
               '241', '151', '444', '253', '452']

    simul = Simulator(environment=target_env,
                      setup=setup_time,
                      number_of_jobs=number_of_jobs,
                      operations_per_jobs=operations_per_jobs,
                      number_of_machines=number_of_machines)

    cs = CuckooSearch(popSize=20,
                      maxIter=100000,
                      number_of_jobs=number_of_jobs,
                      operations_per_jobs = operations_per_jobs,
                      number_of_machines = number_of_machines,
                      target_env=target_env,
                      method=simul,
                      output_per_iter=100)

    cs.search()