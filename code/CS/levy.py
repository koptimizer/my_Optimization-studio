import math
import matplotlib.pyplot as plt
import numpy as np

def levy(mu, c, x):
    try:
        y = math.sqrt(0.5/(2*math.pi))*(math.e**(-c/(2*(x-mu)))/(x-mu)**(3/2))
    except:
        y = 0
    return y

if __name__ == "__main__" :
    mu = 0

    xList = []
    yList1 = []
    yList2 = []
    yList3 = []
    yList4 = []

    for i in np.arange(0, 2, 0.001) :
        xList.append(i)
        yList1.append(levy(mu, 0.5, i))
        yList2.append(levy(mu, 1, i))
        yList3.append(levy(mu, 2, i))
        yList4.append(levy(mu, 4, i))

    plt.plot(xList, yList1)
    plt.plot(xList, yList2)
    plt.plot(xList, yList3)
    plt.plot(xList, yList4)
    plt.legend(["c=0.5", "c=1", "c=2", "c=4"])
    plt.show()


