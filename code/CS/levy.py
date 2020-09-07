import math
import matplotlib.pyplot as plt
import numpy as np

def levy(mu, c, x) :
    y = math.sqrt(0.5/(2*math.pi))*(math.e**(-c/(2*(x-mu)))/(x-mu)**(3/2))
    return y

if __name__ == "__main__" :
    mu = 0

    xList = []
    yList1 = []
    yList2 = []
    yList3 = []

    for i in np.arange(0.001, 1.000, 0.001) :
        xList.append(i)
        yList1.append(levy(mu, 0.5, i))
        yList2.append(levy(mu, 1, i))
        yList3.append(levy(mu, 2, i))

    plt.plot(xList, yList1)
    plt.plot(xList, yList2)
    plt.plot(xList, yList3)
    plt.show()


