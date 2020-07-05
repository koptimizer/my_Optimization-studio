import numpy as np
import random
from collections import defaultdict

# 문제 구성 : {
#   state : {x1, x2, x3, x4, x5, x6}
#   action : {1, 0}
#   reward : {1, -1}
#   if prev_state_fp == 0,1,0,1,0 and currentAction == 0 {
#       reward : 1000}}

# Q-table의 원소 수 : 12개

class QLearningAgent:
    def __init__(self) :
        self.actions = [0, 1]
        self.discountFactor = 0.9
        self.epsilon = 0.1
        self.q_table = {"1": 0, "0": 0,
                        "00": 0, "01": 0, "10": 0, "11": 0,
                        "000": 0, "001": 0, "011": 0, "010": 0, "100": 0, "101": 0, "111": 0, "110": 0,
                        "0000": 0, "0001": 0, "0010": 0, "0011": 0, '0100': 0, '0101': 0, '0110': 0, "0111": 0,
                        '1000': 0, '1001': 0, '1010': 0, '1011': 0, '1100': 0, '1101': 0, '1110': 0, "1111": 0,
                        '00000': 0, '00001': 0, '00010': 0, '00011': 0, '00100': 0, '00101': 0, '00110': 0, '00111': 0,
                        '01000': 0, '01001': 0, '01010': 0, '01011': 0, '01100': 0, '01101': 0, '01110': 0, '01111': 0,
                        '10000': 0, '10001': 0, '10010': 0, '10011': 0, '10100': 0, '10101': 0, '10110': 0, '10111': 0,
                        '11000': 0, '11001': 0, '11010': 0, '11011': 0, '11100': 0, '11101': 0, '11110': 0, '11111': 0,
                        "000000": 0, "000001": 0, "000010": 0, "000011": 0, '000100': 0, '000101': 0, '000110': 0, '000111': 0,
                        "001000": 0, "001001": 0, "001010": 0, "001011": 0, '001100': 0, '001101': 0, '001110': 0, '001111': 0,
                        "010000": 0, "010001": 0, "010010": 0, "010011": 0, '010100': 0, '010101': 0, '010110': 0, '010111': 0,
                        "011000": 0, "011001": 0, "011010": 0, "011011": 0, '011100': 0, '011101': 0, '011110': 0, '011111': 0,
                        "100000": 0, "100001": 0, "100010": 0, "100011": 0, '100100': 0, '100101': 0, '100110': 0, '100111': 0,
                        "101000": 0, "101001": 0, "101010": 0, "101011": 0, '101100': 0, '101101': 0, '101110': 0, '101111': 0,
                        "110000": 0, "110001": 0, "110010": 0, "110011": 0, '110100': 0, '110101': 0, '110110': 0, '110111': 0,
                        '111000': 0, "111001": 0, "111010": 0, "111011": 0, "111100": 0, '111101': 0, '111110': 0, '111111': 0
                        }

    # s, a, r, s`를 이용해서 q-table 업데이트
    def learn(self, state, action, reward, nextState) :
        q_1 = self.q_table[state+str(action)]
        q_2 = reward + self.discountFactor * self.q_table[nextState+self.get_actionOfState(nextState)]
        self.q_table[state+str(action)] += (q_2 - q_1)

    # 마지막 state(6번째 갈림 길)일 때의 q-table 업데이트
    def learnFinal(self, state, action, reward):
        q_1 = reward
        self.q_table[state+str(action)] += q_1

    # e-greedy 정책에 따른 q-table내 해당 state의 action 반환
    def get_action(self, state) :
        if np.random.rand() < self.epsilon :
            action = np.random.choice(self.actions)
        else :
            action = self.get_actionOfState(state)
        return action

    # 최적의 action 반환
    def get_actionOfState(self, state):
        zeroValues = self.q_table[str(state)+'0']
        oneValues = self.q_table[str(state)+'1']
        if zeroValues >= oneValues:
            action = '0'
        else:
            action = '1'
        return action

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

    def toNextState(self, aciton):
        self.currentState += str(action)

    # 현재 action에 대한 reward 반환
    def getReward(self, action):
        reward = 0
        #
        if self.currentState == "01010" and action == '0' :
            reward = 100000
        else :
            if action == '1' :
                reward = 1
            elif action == '0' :
                reward = -1
        return reward

    # episode가 끝날 때마다 다시 environment 세팅
    def setInit(self):
        self.currentState = ""

if __name__ == "__main__" :
    # environment와 agent 초기화
    cop = CoProblem()
    agent = QLearningAgent()

    for episode in range(100000) :
        # episode가 시작할 때마다 environment 초기화
        cop.setInit()
        for stage in range(1,7):
            # state 관측
            state = cop.getCurrentState()
            # state에 따른 action 선택
            action = agent.get_action(state)
            # action에 대한 reward 획득
            reward = cop.getReward(action)

            if len(cop.currentState) != cop.fieldSize-1:
                # nextState 관측
                nextState = cop.getNextState(action)
                # s, a, r, s`를 이용한 학습
                agent.learn(state, action, reward, nextState)
                #print(cop.currentState)
            elif len(cop.currentState) == cop.fieldSize-1:
                cop.toNextState(action)
                # 마지막 단계일 때, s, a, r을 이용한 학습
                agent.learnFinal(state, action, reward)

        print(episode, "episode's totoal state :",  cop.currentState, "total rewards :", agent.q_table[cop.currentState])