import time

class Machine :
    def __init__(self, endTime=20, sequence=[]):
        self.endTime = endTime
        self.sequence = sequence

    def initialize(self):
        print("...Machine을 초기화하고 있습니다...")
        self.eventList = [] # Event list
        self.time = 0 # 현재 시간
        self.comJobs = 0 # Number of complete jobs
        self.isIdle = True # is it Idle?
        self.system = [] # A job allocated to the machine
        self.queue = [] # Jobs waiting for the machine
        self.index = 0 #  job's index
        self.totalWaitingTime = 0

        finish = [-1, self.endTime, 'end']
        self.eventList.append(finish)
        self.eventList.append(self.getJobArr(self.sequence[self.index]))
        self.sortEventList()

        print("CLOCK :", self.time)
        print('Initial Event List :', self.eventList)
        print('현재 가동중인 job :', self.system)
        print('현재 대기중인 job :', self.queue)
        print('유휴 여부 :', self.isIdle, end='\n\n')

    def sortEventList(self):
        self.eventList = sorted(self.eventList, key=lambda x : x[1])

    def getJobArr(self, job):
        # job num, arrival time, event type, processing time
        temp = [job[0], job[1], 'arr', job[3]]
        return temp

    def getJobDep(self, job):
        # job num, departure time, event type
        temp = [job[0], self.time+job[3], 'dep']
        return temp

    def simulation(self):
        self.initialize()
        print("...Simulation을 시작합니다...")
        while 1 :
            time.sleep(1)
            self.time = self.eventList[0][1] # descrete time shift
            # machine allocation part
            if self.eventList[0][2] == 'arr' : # 1) 발생 이벤트가 arrival인 경우
                print('Event type :', self.eventList[0], 'arrival')
                if self.isIdle == False : # 1-1) 가동상태인 경우
                    self.queue.append(self.eventList[0])
                elif self.isIdle == True : # 1-2) 유휴상태인 경우
                    self.system.append(self.eventList[0])
                    self.isIdle = False
                    self.eventList.append(self.getJobDep(self.system[0])) # job dep 업데이트
                    self.index += 1
                    try :
                        self.eventList.append(self.getJobArr(self.sequence[self.index])) # job arr 업데이트
                    except :
                        print("더 이상 작업 불가")
                del self.eventList[0]
                self.sortEventList()
            elif self.eventList[0][2] == 'dep' : # 2) 발생 이벤트가 departure인 경우
                print('Event type :', self.eventList[0], 'departure')
                if self.queue == [] : # 2-1) 대기 큐가 비어있는 경우
                    self.isIdle = True
                else : # 2-2) 대기 큐에 job이 하나 이상 있는 경우
                    self.totalWaitingTime += self.queue[0][-1]
                    self.system.append(self.queue[0])
                    del self.queue[0]
                self.sortEventList()
                del self.system[0]
                del self.eventList[0]
                if self.system != [] : # 2-3) departure후 머신에 할당되었을 때, event List 업데이트
                    self.eventList.append(self.getJobDep(self.system[0]))
                else :
                    self.isIdle = True
                self.comJobs += 1
            elif self.eventList[0][2] == 'end' : # 3) 발생 이벤트가 end인경우
                self.time = self.eventList[0][1]
                print('Event type : The end of the simulation')
                print("CLOCK :", self.time)
                print('Event List :', self.eventList)
                print('현재 가동중인 job :', self.system)
                print('현재 대기중인 job :', self.queue)
                print('유휴 여부 :', self.isIdle)
                print('Total waiting time :', self.totalWaitingTime)
                print('Number of completed jobs :', self.comJobs, end='\n\n')
                print("...시뮬레이션을 종료합니다...")
                return

            # 부품 도착
            try :
                if self.eventList[0][2] == 'dep' or self.eventList[0][2] == 'end':
                    self.index += 1
                    self.eventList.append(self.getJobArr(self.sequence[self.index]))
                    self.sortEventList()
            except :
                pass

            self.sortEventList()
            print("CLOCK :", self.time)
            print('Event List :', self.eventList)
            print('현재 가동중인 job :', self.system)
            print('현재 대기중인 job :', self.queue)
            print('유휴 여부 :', self.isIdle)
            print('Total Waiting Time :', self.totalWaitingTime, end='\n\n')

if __name__ == "__main__" :
    eventlist = [
        # Job index / Arrival time / Interarrival time / Processing time
        [1, 0, 1.73, 2.90], [2, 1.73, 1.35, 1.76], [3, 3.08, 0.71, 3.39],
        [4, 3.79, 0.62, 4.52], [5, 4.41, 14.28, 4.46], [6, 18.69, 0.70, 4.36],
        [7, 19.39, 15.52, 2.07], [8, 34.91, 3.15, 3.36], [9, 38.06, 1.76, 2.37], [10, 39.82, 1.00, 5.38]
    ]
    machine = Machine(endTime=40, sequence=eventlist)
    machine.simulation()