import numpy as np
import random as rd
import math as mt
import sys
from collections import defaultdict

class Machine :
    def __init__(self, setup, number):
        self.index = 0 # Machine이 예정된 operation 중 현재 할당 할 Operation의 위치
        self.isIdle = True # Idle 상태 여부
        self.setup = setup # 2차원 List 형태의 Setup info를 불러와서 저장
        self.number = number # Machine의 고유번호
        self.recentSetup = 0 # Machine의 현재 setup 상태
        self.queue = [] # 현재 Machine에서의 대기 Operation들
        self.system = [] # 기계 안에서 처리중인 Operation

    # Machine에서 처리될 operation 할당
    def allocation(self, info):
        self.system.append(info)
        self.isIdle = False
        self.recentSetup = int(info[0])
        return info

    # Machine에서 처리중인 operation 해제
    def deallocation(self):
        self.system.pop()
        self.isIdle = True

class Simulator :
    def __init__(self, environment, setup, number_of_jobs, operations_per_jobs, number_of_machines):
        print('...Simulator를 초기화중입니다...')
        self.environment = environment # 3차원 List 형태의 FJSP info를 불러와서 저장
        self.number_of_jobs = number_of_jobs # Job의 개수
        self.operations_per_jobs = operations_per_jobs # Job당 Operation의 갸수
        self.number_of_machines = number_of_machines # Machine의 개수
        self.setup = setup # 2차원 List 형태의 Setup info를 불러와서 저장

        self.machineList = [] # Machine 객체들을 저장할 List
        self.operationSequencePerMachine = [] # Machine 별 Operation 순서
        self.machineInit() # Machine Initalization 함수

        self.eventlist = [] # ['Type', Job, Operation, Machine, Processing(orSetup)Time, FinishTime]
        self.TNOW = 0
        self.index = 0 # 기록을 위한 변수, entity 처리 순서를 나타냄
        self.WIP = defaultdict()
        print('Simulating 준비가 모두 끝났습니다.')

    # 여러번의 시뮬레이션을 위한 변수초기화 함수
    def initialize(self):
        self.eventlist = []
        self.TNOW = 0
        self.index = 0
        self.WIP = defaultdict()
        self.completer = []
        self.operationSequencePerMachine = []
        self.machineInit()

    # Machine 객체의 변수초기화 함수
    def machineInit(self):
        for i in range(1, self.number_of_machines+1) :
            self.machineList.append(Machine(self.setup[i-1], i))
            self.operationSequencePerMachine.append([])
            self.machineList[i-1].index = 0
            self.machineList[i-1].recentSetup = 0

    # Eventlist를 EndTime 순으로 Sorting 하는 함수
    def sortEventlist(self):
        self.eventlist = sorted(self.eventlist, key=lambda x : x[-1])

    def feasibleChecker(self):
        # TODO Fully Feasible 체커는 좀 나중에 구현하는 걸로... 방법은 J,O 떼와서 정렬인지 확인 + M할당 적합성 확인?
        return True

    # JOM의 Setup info를 반환하는 함수, Setup이 필요 없을 경우 None 반환
    def getSetupInfo(self, JOM):
        alloc_machine = self.machineList[int(JOM[2]) - 1]
        job = int(JOM[0])
        operation = int(JOM[1])
        machine = int(JOM[2])
        setupTime = 0
        finishTime = 0

        if alloc_machine.recentSetup != job and alloc_machine.recentSetup != 0 :
            setupTime = self.setup[int(job) - 1][alloc_machine.recentSetup - 1]

        if setupTime != 0 :
            finishTime = self.TNOW + setupTime
            return ['Set', job, operation, machine, setupTime, finishTime]
        else :
            return None

    # JOM이 할당될 수 없을 때, Waiting event로 반환해주는 함수
    def getWaitingInfo(self, JOM):
        alloc_machine = self.machineList[int(JOM[2]) - 1]
        job = int(JOM[0])
        operation = int(JOM[1])
        machine = int(JOM[2])
        processingTime = 0
        finishTime = sys.maxsize

        return ['Wat', job, operation, machine, processingTime, finishTime]

    # JOM이 할당될 수 있을 때, Departure event로 반환해주는 함수
    def getDepartureInfo(self, JOM):
        alloc_machine = self.machineList[int(JOM[2]) - 1]
        job = int(JOM[0])
        operation = int(JOM[1])
        machine = int(JOM[2])
        processingTime = self.environment[job-1][operation-1][machine-1]
        finishTime = self.TNOW + processingTime

        # 해당 Machine에 해당 Entity를 할당
        alloc_machine.allocation([job, operation, machine, processingTime, finishTime])

        return ['Dep', job, operation, machine, processingTime, finishTime]

    # index당 eventlist 및 TNOW 출력 함수
    def output_per_index(self):
        print(self.index, "번 째 Event list :", self.eventlist, 'TNOW : ', self.TNOW)

    # Machine 별로 Operation Sequence를 정해주는 함수
    def getOperationSequencePerMachine(self):
        for i in self.solution :
            self.operationSequencePerMachine[int(i[2])-1].append(i)

    def simulate(self, solution):
        self.initialize() # 여러 번의 시뮬레이션을 위해 초기화
        self.solution = solution
        if self.feasibleChecker() == False : # 모든 해가 유효하게 가정 및 유도
            print("해가 유효하지 않습니다.")
            return

        # print(solution)
        self.getOperationSequencePerMachine() # Operation Sequence 산출
        setupTime = None
        # print(self.operationSequencePerMachine)

        # eventlist의 초기할당
        for i in range(self.number_of_machines) :
            try :
                if self.operationSequencePerMachine[i][0][1] == '1' :
                    todo = self.operationSequencePerMachine[i][0]
                    setupTime = self.getSetupInfo(todo)
                    if setupTime == None :
                        pass
                    else :
                        self.eventlist.append(setupTime)
                    self.eventlist.append(self.getDepartureInfo(todo))
                else :
                    todo = self.operationSequencePerMachine[i][0]
                    self.eventlist.append(self.getWaitingInfo(todo))
            except :
                pass
        self.sortEventlist()

        # 예정된 이벤트들이 종료될 때 까지 시뮬레이션
        while self.eventlist != [] :
            self.index += 1 # 인덱스 +1
            # self.output_per_index()
            self.TNOW = self.eventlist[0][-1]
            if self.eventlist[0][0] == 'Set' : # setup 이벤트일 경우 처리 후, Departure 이벤트로 변환 및 해당 루프 종료
                todo = str(self.eventlist[0][1]) + str(self.eventlist[0][2]) + str(self.eventlist[0][3])
                self.eventlist.append(self.getDepartureInfo(todo))
                self.machineList[int(self.eventlist[0][3]) - 1].index += 1
                self.eventlist.pop(0)
                self.sortEventlist()
                continue
            currenter = self.operationSequencePerMachine[int(self.eventlist[0][3]) - 1][self.machineList[int(self.eventlist[0][3]) - 1].index]  # 현재 가리키는 JOM
            self.machineList[int(self.eventlist[0][3]) - 1].deallocation() # JOM을 할당 해제하고 WIP에 삽입
            try :
                self.WIP[currenter[0:2]] += 1  # JO
            except :
                self.WIP[currenter[0:2]] = 1

            # 해당 Machine에서 다음에 올 J'O'M을 이벤트 리스트에 삽입(할당 가능 시 Set or Dep 이벤트 발생, 불가능시 Wat 이벤트 발생)
            try :
                nexter = self.operationSequencePerMachine[int(currenter[-1])-1][self.machineList[int(self.eventlist[0][3]) - 1].index+1]
                self.eventlist.pop(0)
                if str(int(nexter[0:2]) - 1) in list(self.WIP.keys()) or nexter[1] == '1':
                    todo = nexter
                    setup = self.getSetupInfo(todo)
                    if setup == None:
                        self.eventlist.append(self.getDepartureInfo(todo))
                        self.machineList[int(nexter[-1]) - 1].index += 1
                    else:
                        self.eventlist.append(setup)
                else:
                    self.eventlist.append(self.getWaitingInfo(nexter))
                self.sortEventlist()
            except :
                self.eventlist.pop(0)

            for i in range(len(self.eventlist)) :
                if self.eventlist[i][5] == sys.maxsize :
                    todo = str(self.eventlist[i][1]) + str(self.eventlist[i][2]) + str(self.eventlist[i][3])
                    if str(int(todo[0:2])-1) in list(self.WIP.keys()) :
                        setup = self.getSetupInfo(todo)
                        if setup == None:
                            self.eventlist.append(self.getDepartureInfo(todo))
                            if self.operationSequencePerMachine[int(todo[-1]) - 1][0] != todo : # 예외 지정
                                self.machineList[int(todo[-1]) - 1].index += 1
                        else:
                            self.eventlist.append(setup)
                        self.eventlist.pop(i)
                        self.sortEventlist()

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

    setup_time = [[0, 4, 2, 4],
                  [2, 0, 2, 3],
                  [1, 5, 0, 1],
                  [4, 4, 4, 0]]

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

    cuckoor = ['411', '421', '212', '434', '314',
               '441', '113', '452', '324', '121',
               '333', '132', '344', '141', '153',
               '353', '223', '232', '244', '253']

    simul = Simulator(environment=target_env,
                      setup=setup_time,
                      number_of_jobs=number_of_jobs,
                      operations_per_jobs=operations_per_jobs,
                      number_of_machines=number_of_machines)

    # print(simul.simulate(cuckoor))


    cs = CuckooSearch(popSize=20,
                      maxIter=100000,
                      number_of_jobs=number_of_jobs,
                      operations_per_jobs = operations_per_jobs,
                      number_of_machines = number_of_machines,
                      target_env=target_env,
                      method=simul,
                      output_per_iter=100)

    cs.search()