import math

def boothFunc(x, y):
    # min(1, 3) = 0
    if x < -10 or x > 10 or y < -10 or y > 10:
        print("Input Error")
        exit(1)
    else:
        z = (x + 2*y - 7)**2 + (2*x + y - 5)**2
        return z

def matyasFunc(x, y):
    # min(0, 0) = 0
    if x < -10 or x > 10 or y < -10 or y > 10:
        print("Input Error range : -10 ~ 10")
        exit(1)
    else:
        z = 0.26*(x**2 + y**2) - 0.48*x*y
        return z

def ackleyFunc(x, y):
    # min(0, 0) = 0
    if x < -5 or x > 5 or y < -5 or y > 5:
        print("Input Error range : -5 ~ 5")
        exit(1)
    else:
        z = -20*math.exp(math.fabs(-0.2*math.sqrt(0.5*(x**2 + y**2)))) - math.exp(math.fabs(0.5*(math.cos(2*x*math.pi) + math.cos(2*y*math.pi)))) + math.e + 20
        return z

def levi13Func(x, y):
    # min(1, 1) = 0
    if x < -10 or x > 10 or y < -10 or y > 10:
        print("Input Error range : -10 ~ 10")
        exit(1)
    else:
        z = (math.sin(3*x*math.pi))**2 + ((x - 1)**2)*(1 + math.sin(3*y*math.pi)**2) + ((y - 1)**2)*(1 + math.sin(2*y*math.pi)**2)
        return round(z, 10)

def himmelblauFunc(x, y):
    # min(3, 2) = 0
    # min(-2.805118, 3.131312) = 0
    # min(-3.779310, -3.283186) = 0
    # min(3.584428, -1.848126) = 0
    if x < -5 or x > 5 or y < -5 or y > 5:
        print("Input Error range : -5 ~ 5")
        exit(1)
    else:
        z = (x**2 + y - 11)**2 + (x + y**2 - 7)**2
        return round(z, 10)

def bealeFunc(x, y):
    # min(3, 0.5) = 0
    if x < -4.5 or x > 4.5 or y < -4.5 or y > 4.5:
        print("Input Error range : -4.5 ~ 4.5")
        exit(1)
    else:
        z = (1.5 - x + x*y)**2 + (2.25 - x + x*(y**2))**2 + (2.625 - x + x*(y**3))**2
        return z

def goldsteinPriceFunc(x, y):
    # min(0, -1) = 3
    if x < -2 or x > 2 or y < -2 or y > 2:
        print("Input Error")
        exit(1)
    else:
        z = ((1 + (x + y + 1)**2 * (19 - 14*x + 3*(x**2) - 14*y + 6*x*y + 3*(y**2))) * (30 + (2*x - 3*y)**2 * (18 - 32*x + 12*(x**2) + 48*y - 36*x*y + 27*(y**2))))
        return z