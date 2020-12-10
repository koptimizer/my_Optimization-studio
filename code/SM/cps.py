import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.expand_frame_repr', False) # DataFrame 출력시 짤림 해결
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)

class Machine :
    # ['Set', job, operation, machine, processingTime, start]
    def __init__(self, setup, number):
        print('...'+str(number)+'번 Machine를 초기화중입니다...')
        self.isIdle = True
        self.setup = setup
        self.number = number
        self.machine_time = 0
        self.recentSetup = np.nan
        self.queue = [] # 아직 못들어간 대기 엔티티들
        self.system = [] # 기계 안에서 직접 할당중인 엔티티

    def allocation(self, info):
        info[5] += info[4]
        self.system.append(info)
        self.isIdle = False
        self.recentSetup = info[1]
        return info

    def deallocation(self):
        self.machine_time = int(self.system[0][-1]) + int(self.system[0][-2])
        self.system.pop()
        self.isIdle = True

    def deallocation_queue(self):
        self.machine_time += int(self.system[4]) + int(self.system[5])
        depinfo = self.pop_queue()
        self.system.pop()
        self.allocation(self.pop_queue())
        return depinfo

    def insert_queue(self, entity):
        self.queue.append(entity)

    def pop_queue(self):
        poper = self.queue[0]
        self.queue.pop(0)
        return poper

class Simulator :
    def __init__(self, environment, setup, number_of_jobs, operations_per_jobs, number_of_machines):
        print('...Simulator를 초기화중입니다...')
        self.environment = environment
        self.env_info = self.env_to_info()
        self.number_of_jobs = number_of_jobs
        self.operations_per_jobs = operations_per_jobs
        self.number_of_machines = number_of_machines
        self.setup = setup
        self.machineInit()
        self.eventlist = []
        self.TNOW = 0
        self.index = 0
        self.todo = None
        self.waiter = [[], [], [], []]
        self.jobTime = [0, 0, 0, 0]
        print('Simulating 준비가 모두 끝났습니다.')

    def env_to_info(self) :
        return

    def machineInit(self):
        self.machineList = []
        for i in range(1, self. number_of_machines+1) :
            self.machineList.append(Machine(self.setup[i-1], i))

    def sortEventlist(self):
        self.eventlist = sorted(self.eventlist, key=lambda x : x[-1])

    def feasibleChecker(self):
        # TODO Fully Feasible 체커는 좀 나중에 구현하는 걸로... 방법은 J,O 떼와서 정렬인지 확인 + M할당 적합성 확인?
        return True

    def getArrivalInfo(self, JOM):
        alloc_machine = self.machineList[int(JOM[2]) - 1]
        job = JOM[0]
        operation = JOM[1]
        machine = JOM[2]
        start = 100
        # get processing time
        processingTime = self.environment[int(job)-1][int(operation)-1][int(machine)-1]

        # get processing time + setup
        if np.isnan(alloc_machine.recentSetup):
            processingTime += alloc_machine.setup[int(job) - 1]  # 디폴트 셋업
        elif alloc_machine.recentSetup != job:
            processingTime += alloc_machine.setup[alloc_machine.recentSetup - 1]

        if self.jobTime[int(JOM[0]) - 1] <= alloc_machine.machine_time:
            start = self.jobTime[int(JOM[0]) - 1]
        elif self.jobTime[int(JOM[0]) - 1] >= alloc_machine.machine_time:
            start = alloc_machine.machine_time

        return ['Arr', job, operation, machine, processingTime, start]

    def getDepartureInfo(self, info):
        info[0] = 'Dep'
        return info

    def output_per_index(self):
        print(self.index, "번 째 Event list :", self.eventlist, 'TNOW : ', self.TNOW)

    def simulate(self, solution):
        self.solution = solution
        if self.feasibleChecker() == False : # 모든 해가 유효하게 가정 및 유도
            print("해가 유효하지 않습니다.")
            return
        while 1 :
            todo = self.solution[0]
            self.solution.pop(0)
            self.eventlist.append(self.getArrivalInfo(todo))


        self.eventlist.append(['End', 9999, 9999, 9999, 9999, 9999])
        self.output_per_index()

        while self.eventlist[0][0] != 'End' :
            self.index += 1 # 인덱스 +1
            if self.eventlist[0][0] == 'Arr' :
                if self.machineList[int(self.eventlist[0][3]) - 1].isIdle : # 유휴상태 시
                    depinfo = self.machineList[int(self.eventlist[0][3]) - 1].allocation(self.eventlist[0])
                    self.eventlist.append(self.getDepartureInfo(depinfo))
                    self.TNOW = self.eventlist[0][-1]
                    self.eventlist.pop(0)
                    self.sortEventlist()
                    self.output_per_index()
                else : # 가동상태 시
                    self.machineList[int(self.eventlist[0][3]) - 1].insert_queue(self.eventlist[0])
                    self.TNOW = self.eventlist[0][-1]
                    self.eventlist.pop(0)
                    self.sortEventlist()
                    self.output_per_index()

            elif self.eventlist[0][0] == 'Dep' :
                if self.machineList[int(self.eventlist[0][3])-1].queue == [] :
                    self.machineList[int(self.eventlist[0][3])-1].deallocation()
                    self.TNOW = self.eventlist[0][-1]
                    self.jobTime[int(self.eventlist[0][1])-1] = self.TNOW
                    self.eventlist.pop(0)
                    self.sortEventlist()

                    todo = self.solution[0]
                    self.solution.pop(0)
                    self.eventlist.append(self.getArrivalInfo(todo))
                    self.sortEventlist()
                    self.output_per_index()

                elif self.machineList[int(self.eventlist[0][3])-1].queue != [] :
                    depinfo = self.machineList[int(self.eventlist[0][3]) - 1].deallocation_queue()
                    self.eventlist.append(self.getDepartureInfo(depinfo))
                    self.TNOW = self.eventlist[0][-1]
                    self.jobTime[int(self.eventlist[0][1]) - 1] = self.TNOW
                    self.eventlist.pop(0)
                    self.sortEventlist()

                    todo = self.solution[0]
                    self.solution.pop(0)
                    self.eventlist.append(self.getArrivalInfo(todo))
                    self.sortEventlist()
                    self.output_per_index()

            else :
                return



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

    solution = ['111', '212', '314', '413', '121',
                '223', '322', '423', '131', '232',
                '333', '434', '143', '241', '342',
                '444', '154', '253', '352', '452']

    simul = Simulator(environment=target_env,
                      setup=setup_time,
                      number_of_jobs=number_of_jobs,
                      operations_per_jobs=operations_per_jobs,
                      number_of_machines=number_of_machines)

    simul.simulate(solution=solution)