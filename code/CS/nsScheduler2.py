import pandas as pd
import numpy as np
import datetime
import random
import joblib
import xgboost as xgb
import math

class DCS():
    def __init__(self, populationSize, pa, pc, model, load=None) :
        self.popSize = populationSize # 해집단 크기
        self.pa = pa # pa가 높을수록 해를 찾는 속도는 빨라지지만, 설익은 수렴을 할 가능성이 높아집니다.
        self.pc = pc # pc가 높을수록 더 좋은 해를 찾을 수 있게 가이드해주지만, 설익은 수렴을 할 가능성이 높아집니다.
        self.population = []
        self.broadTimeList = [20,20,20,20,20,20,20,40,40,60]
        self.model = model
        self.dataFrame = []
        self.dataSet = {"mother_code" : 0, "product_code" : 0, "name_code" : 0, "type_code" : 0, "price_code" : 0,
                      "bcDateTime" : 0, "objTime" : 0}
        self.load = load

    def getSeason(self, x):
        if (x < 3) | (x == 12):
            return 3
        elif (x >= 3) & (x < 6):
            return 0
        elif (x >= 6) & (x < 9):
            return 1
        else:
            return 2

    def setData(self):
        self.dataFrame = pd.read_excel("submission.xlsx")
        self.dataFrame.drop(['취급액'], axis=1, inplace=True)
        self.dataFrame = self.dataFrame.dropna(axis=0)
        dropIdx = self.dataFrame[self.dataFrame['상품군'] == "무형"].index
        self.dataFrame = self.dataFrame.drop(dropIdx)

    def init(self):
        self.setData()
        for p in range(self.popSize) :
            if p == 0 and self.load != None :
                loadDf = pd.read_csv(self.load, encoding="utf-8-sig")
                self.population.append(loadDf)
                pass
            schedule = []
            self.dataSet["mother_code"] = self.dataFrame["마더코드"].tolist()
            self.dataSet["product_code"] = self.dataFrame["상품코드"].tolist()
            self.dataSet["name_code"] = self.dataFrame["상품명"].tolist()
            self.dataSet["type_code"] = self.dataFrame["상품군"].tolist()
            self.dataSet["price_code"] = self.dataFrame["판매단가"].tolist()
            self.dataSet["bcDateTime"] = datetime.datetime(2020, 6, 1, 6, 0, 0)
            self.dataSet["objTime"] = datetime.datetime(2020, 7, 1, 2, 0, 0)
            while self.dataSet["bcDateTime"] < self.dataSet["objTime"] :
                if self.dataSet["bcDateTime"].strftime("%H") == "02" :
                    self.dataSet["bcDateTime"] = self.dataSet["bcDateTime"] + datetime.timedelta(hours=4)
                    temp_ti = 20
                    self.dataSet["bcDateTime"] = self.dataSet["bcDateTime"] + datetime.timedelta(minutes=temp_ti)
                elif self.dataSet["bcDateTime"].strftime("%H") == "01" :
                    temp_ti = 20
                    self.dataSet["bcDateTime"] = self.dataSet["bcDateTime"] + datetime.timedelta(minutes=temp_ti)
                else :
                    temp_ti = random.sample(self.broadTimeList, 1)[0]
                    self.dataSet["bcDateTime"] = self.dataSet["bcDateTime"] + datetime.timedelta(minutes=temp_ti)

                tempRand = random.randrange(len(self.dataSet["mother_code"]))
                temp_mc = self.dataSet["mother_code"][tempRand]
                del self.dataSet["mother_code"][tempRand]
                temp_dc = self.dataSet["product_code"][tempRand]
                del self.dataSet["product_code"][tempRand]
                temp_nc = self.dataSet["name_code"][tempRand]
                del self.dataSet["name_code"][tempRand]
                temp_tc = self.dataSet["type_code"][tempRand]
                del self.dataSet["type_code"][tempRand]
                temp_pc = self.dataSet["price_code"][tempRand]
                del self.dataSet["price_code"][tempRand]
                temp_month = self.dataSet["bcDateTime"].month
                temp_day = self.dataSet["bcDateTime"].day
                temp_hour = self.dataSet["bcDateTime"].hour
                temp_minute = self.dataSet["bcDateTime"].minute
                temp_weekday = self.dataSet["bcDateTime"].weekday()
                temp_season = self.getSeason(temp_month)
                temp_holiday = 0
                if temp_month == 6 and temp_day == 6 :
                    temp_holiday = 1

                temp = [self.dataSet["bcDateTime"].strftime("%Y-%m-%d %H:%M:%S"), temp_ti, temp_mc, temp_dc, temp_nc, temp_tc, temp_pc,
                        np.nan, temp_month, temp_day, temp_hour, temp_minute, temp_weekday, temp_season, temp_holiday]
                schedule.append(temp)
                print(self.dataSet["bcDateTime"].strftime("%Y-%m-%d %H:%M:%S"))

            schedule = pd.DataFrame(schedule)
            schedule.columns = ['방송일시', '노출(분)', '마더코드', '상품코드', '상품명', '상품군', '판매단가', '취급액', 'month', 'day', 'hour', 'minute', 'weekday', 'season', 'holiday']
            schedule['방송일시'] = pd.to_datetime(schedule['방송일시'], format="%Y-%m-%d %H:%M:%S")

            schedule = self.getFitness(schedule)
            self.population.append(schedule)
        self.population.sort(key=lambda x : x["취급액"].sum(), reverse=True)

    def getProductCode(self, x):
        d1 = {'의류': 1, '속옷': 2, '주방': 3, '농수축': 4, '이미용': 5, '가전': 6, '생활용품': 7,
              '건강기능': 8, '잡화': 9, '가구': 10, '침구': 11, '무형': 12}
        return d1[x]

    def getFitness(self, schedule):
        cols = ['노출(분)', '마더코드', '상품코드', '상품군', '판매단가', 'day', 'hour', 'minute', 'weekday', 'season', 'holiday']
        ori_cols = ['방송일시', '노출(분)', '마더코드', '상품코드', '상품명', '상품군', '판매단가', '취급액']
        test_original = schedule
        test = test_original[cols]
        test.loc[:, '상품군'] = test.loc[:, '상품군'].map(self.getProductCode)
        model = joblib.load(self.model)

        predictions = model.predict(xgb.DMatrix(test), ntree_limit=model.best_iteration)
        test_pred = test['판매단가'] * predictions
        test_pred = test_pred.round(-3)
        test_original['취급액'] = test_pred
        test_original = test_original[ori_cols]
        # test_original.to_excel("pred"+self.filename)
        # fitness = test_original['취급액'].sum()
        # self.fitness.append(fitness)
        return test_original

    def getLevy(self):
        return math.pow(random.uniform(0.0001, 0.9999), -1.0 / 3.0)

    def getDoubleBridge(self, schedule):
        points = sorted(random.sample(range(0, len(schedule.index)), 2))
        newTime = datetime.datetime.strptime(str(schedule["방송일시"].iloc[points[0]]), "%Y-%m-%d %H:%M:%S")
        part = schedule.iloc[points[0]:points[1]].copy()
        part = part.iloc[::-1]

        schedule.iloc[points[0]:points[1]] = part

        for index in range(points[0], points[1]):
            if newTime.strftime("%H") == "02":
                newTime += datetime.timedelta(hours=4, minutes=int(schedule["노출(분)"].iloc[index]))
                schedule["방송일시"].iloc[index] = newTime
            else:
                newTime += datetime.timedelta(minutes=int(schedule["노출(분)"].iloc[index]))
                schedule["방송일시"].iloc[index] = newTime
        return schedule

    def getTwoOpt(self, schedule):
        points = sorted(random.sample(range(0, len(schedule.index)), 2))
        newTime = datetime.datetime.strptime(str(schedule["방송일시"].iloc[points[0]]), "%Y-%m-%d %H:%M:%S")
        part1 = schedule.iloc[points[0]].copy()
        part2 = schedule.iloc[points[1]].copy()

        schedule.iloc[points[1]] = part1
        schedule.iloc[points[0]] = part2
        for index in range(points[0], points[1]):
            if newTime.strftime("%H") == "02" :
                newTime += datetime.timedelta(hours=4, minutes=int(schedule["노출(분)"].iloc[index]))
                schedule["방송일시"].iloc[index] = newTime
            else:
                newTime += datetime.timedelta(minutes=int(schedule["노출(분)"].iloc[index]))
                schedule["방송일시"].iloc[index] = newTime
        return schedule

    def abandon(self):
        schedule = []
        self.dataSet["mother_code"] = self.dataFrame["마더코드"].tolist()
        self.dataSet["product_code"] = self.dataFrame["상품코드"].tolist()
        self.dataSet["name_code"] = self.dataFrame["상품명"].tolist()
        self.dataSet["type_code"] = self.dataFrame["상품군"].tolist()
        self.dataSet["price_code"] = self.dataFrame["판매단가"].tolist()
        self.dataSet["bcDateTime"] = datetime.datetime(2020, 6, 1, 6, 0, 0)
        self.dataSet["objTime"] = datetime.datetime(2020, 7, 1, 2, 0, 0)
        while self.dataSet["bcDateTime"] < self.dataSet["objTime"]:
            if self.dataSet["bcDateTime"].strftime("%H") == "02":
                self.dataSet["bcDateTime"] = self.dataSet["bcDateTime"] + datetime.timedelta(hours=4)
                temp_ti = 20
                self.dataSet["bcDateTime"] = self.dataSet["bcDateTime"] + datetime.timedelta(minutes=temp_ti)
            elif self.dataSet["bcDateTime"].strftime("%H") == "01":
                temp_ti = 20
                self.dataSet["bcDateTime"] = self.dataSet["bcDateTime"] + datetime.timedelta(minutes=temp_ti)
            else:
                temp_ti = random.sample(self.broadTimeList, 1)[0]
                self.dataSet["bcDateTime"] = self.dataSet["bcDateTime"] + datetime.timedelta(minutes=temp_ti)

            tempRand = random.randrange(len(self.dataSet["mother_code"]))
            temp_mc = self.dataSet["mother_code"][tempRand]
            del self.dataSet["mother_code"][tempRand]
            temp_dc = self.dataSet["product_code"][tempRand]
            del self.dataSet["product_code"][tempRand]
            temp_nc = self.dataSet["name_code"][tempRand]
            del self.dataSet["name_code"][tempRand]
            temp_tc = self.dataSet["type_code"][tempRand]
            del self.dataSet["type_code"][tempRand]
            temp_pc = self.dataSet["price_code"][tempRand]
            del self.dataSet["price_code"][tempRand]
            temp_month = self.dataSet["bcDateTime"].month
            temp_day = self.dataSet["bcDateTime"].day
            temp_hour = self.dataSet["bcDateTime"].hour
            temp_minute = self.dataSet["bcDateTime"].minute
            temp_weekday = self.dataSet["bcDateTime"].weekday()
            temp_season = self.getSeason(temp_month)
            temp_holiday = 0
            if temp_month == 6 and temp_day == 6:
                temp_holiday = 1

            temp = [self.dataSet["bcDateTime"].strftime("%Y-%m-%d %H:%M:%S"), temp_ti, temp_mc, temp_dc, temp_nc,
                    temp_tc, temp_pc,
                    np.nan, temp_month, temp_day, temp_hour, temp_minute, temp_weekday, temp_season, temp_holiday]
            schedule.append(temp)
            # print(self.dataSet["bcDateTime"].strftime("%Y-%m-%d %H:%M:%S"))

        schedule = pd.DataFrame(schedule)
        schedule.columns = ['방송일시', '노출(분)', '마더코드', '상품코드', '상품명', '상품군', '판매단가', '취급액', 'month', 'day', 'hour',
                            'minute', 'weekday', 'season', 'holiday']

        schedule = self.getFitness(schedule)
        return schedule

    def evolution(self):
        generation = 0
        self.init()
        while 1 :
            target_num = random.randint(0, int(self.pc * self.popSize))
            target_schedule = self.population[target_num]
            # todo =0으로 바꿔주기
            mod_schedule = self.population[target_num]

            # Get a cuckoo randomly by levy flight
            levyStep = self.getLevy()
            if levyStep > 2 :
                print("doubleBridge")
                mod_schedule = self.getDoubleBridge(target_schedule)
            else :
                print("twoOpt")
                mod_schedule = self.getTwoOpt(target_schedule)

            # Evaluate and replace
            if target_schedule["취급액"].sum() < mod_schedule["취급액"].sum() :
                self.population[target_num] = mod_schedule

            # Pa of worse nests are abandoned and new ones built
            for p in range(self.popSize - int(self.pa*self.popSize), self.popSize):
                self.population[p] = self.abandon()

            self.population.sort(key=lambda x: x["취급액"].sum(), reverse=True)
            generation += 1

            if generation % 300 == 0 :
                fileName = datetime.datetime.now().strftime("%Y%m%d")+"test.csv"
                self.population[0].to_csv(fileName, index=False, encoding="utf-8-sig")
                print(generation, "저장 완료")
                print(self.population[0]["취급액"].sum())
            elif generation % 100 == 0 :
                print(generation, "완료")
                print(self.population[0]["취급액"].sum())
            elif generation % 10 == 0 :
                print(generation, "완료")

if __name__ == "__main__" :
    dcs = DCS(populationSize=20, pa=0.25, pc=0.5, model="base_model_xgb2.model", load="20200926test.csv")
    dcs.evolution()