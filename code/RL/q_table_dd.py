import numpy as np
import timeit
from collections import defaultdict

# 문제 구성 : {
#   state : {x1, x2, x3, x4, x5, x6}
#   action : {1, 0}
#   reward : {1, -1}
#   if prev_state_fp == 0,1,0,1,0 and currentAction == 0 {
#       reward : 1000}
#  }

class QLearningAgent:
    # 상태 변환 확률은 1이므로 생략
    def __init__(self) :
        self.actions = [0, 1]
        self.learningLate = 0.01
        self.discountFactor = 0.99
        self.epsilon = 0.1
        self.q_table = defaultdict(int)

    def setWarmup(self) :
        self.epsilon = 1

    # 최적경로를 찾기까지 epsilon을 1로 설정. 탐색력 최대화
    def adjWarmup(self, str):
        if self.q_table[str] == 9999 and self.epsilon > 0.11 :
            self.epsilon -= 0.1
        else :
            pass

    # s, a, r, s`를 이용해서 q-table 업데이트
    def learn(self, state, action, reward, nextState) :
        q_1 = self.q_table[state+str(action)]
        q_2 = reward + self.discountFactor * self.q_table[nextState+self.argMax(nextState)]
        self.q_table[state+str(action)] += self.learningLate * (q_2 - q_1)

    # 마지막 state(6번째 갈림 길)일 때의 q-table 업데이트
    def learnFinal(self, state, action, reward):
        q_1 = reward
        self.q_table[state+str(action)] = q_1

    # e-greedy 정책에 따른 q-table내 해당 state의 action 반환
    def get_action(self, state) :
        if np.random.rand() < self.epsilon :
            action = np.random.choice(self.actions)
            # print("i'm greedy!")
        else :
            action = self.argMax(state)
        return str(action)

    # 최적의 action 반환
    def argMax(self, state):
        zeroValues = self.q_table[str(state)+'0']
        oneValues = self.q_table[str(state)+'1']
        if zeroValues > oneValues:
            action = '0'
        elif zeroValues < oneValues:
            action = '1'
        else:
            action = str(np.random.choice(self.actions))
        return str(action)

    def diverCheck(self):
        checker = 0
        if self.q_table['0'] >= 100 :
            return True
        else :
            return False

class CoProblem :
    def __init__(self) :
        self.fieldSize = 6 # 최대 행동 수
        self.currentState = "" # 현재 상태

    # 현재 state 반환
    def getCurrentState(self):
        self.currentState
        return self.currentState

    # 다음 state를 반환
    def getNextState(self, action):
        self.currentState += str(action)
        return self.currentState

    # 다음 state로 이동
    def toNextState(self, aciton):
        self.currentState += str(action)

    # 현재 action에 대한 reward 반환
    def getReward(self, action):
        reward = 0
        if self.currentState == "01010" and action == '0' :
            reward += 9999
        else :
            if action == '0':
                reward += -1
            else:
                reward += 1
        return reward

    # episode가 끝날 때마다 다시 environment 세팅
    def setInit(self):
        self.currentState = ""

if __name__ == "__main__" :
    # Max Episode 설정
    MAX_EPISODE = 10000

    # environment와 agent 초기화
    start = timeit.default_timer()
    cop = CoProblem()
    agent = QLearningAgent()

    # 웜업을 통한 초기탐색
    agent.setWarmup()
    for episode in range(MAX_EPISODE) :
        # episode가 시작할 때마다 environment 초기화
        cop.setInit()

        for stage in range(1,7):
            # state 관측
            state = cop.getCurrentState()
            # state에 따른 agent의 action 선택
            action = agent.get_action(state)
            # action에 대한 reward 획득
            reward = cop.getReward(action)

            if len(cop.currentState) != cop.fieldSize-1:
                # state와 action을 이용해서 nextState 관측
                nextState = cop.getNextState(action)
                # s, a, r, s`를 이용한 Q-table 학습
                agent.learn(state, action, reward, nextState)
            elif len(cop.currentState) == cop.fieldSize-1:
                cop.toNextState(action)
                # 마지막 단계일 때, s, a, r을 이용한 Q-table 학습
                agent.learnFinal(state, action, reward)
                # 웜업 조정
        agent.adjWarmup(cop.getCurrentState())
        print(episode, "episode's totoal state :",  cop.currentState, "total rewards :", agent.q_table[cop.currentState])

        # 수렴 확인
        if agent.diverCheck() == True :
            print("i'm god")
            break
    print(agent.epsilon)
    print(agent.q_table)
    stop = timeit.default_timer()
    print(stop - start)