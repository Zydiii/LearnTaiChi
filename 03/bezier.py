import numpy as np
import matplotlib.pyplot as plt


def B_nx(n, i, x):
    if i > n:
        return 0
    elif i == 0:
        return (1-x)**n
    elif i == 1:
        return n*x*((1-x)**(n-1))
    return B_nx(n-1, i, x)*(1-x)+B_nx(n-1, i-1, x)*x

def get_value(p, canshu):
    sumx = 0.
    sumy = 0.
    length = len(p)-1
    for i in range(0, len(p)):
        sumx += (B_nx(length, i, canshu) * p[i][0])
        sumy += (B_nx(length, i, canshu) * p[i][1])
    return sumx, sumy

def get_newxy(p,x):
    xx = [0] * len(x)
    yy = [0] * len(x)
    for i in range(0, len(x)):
        print('x[i]=', x[i])
        a, b = get_value(p, x[i])
        xx[i] = a
        yy[i] = b
        print('xx[i]=', xx[i])
    return xx, yy

p = np.array([                           #控制点，控制贝塞尔曲线的阶数n
    [2, -4],
    [3, 8],
    [5, 1],
    [7, 6],
    [9, 4],
    [7, 1],
])

x = np.linspace(0, 1, 101)
xx, yy = get_newxy(p, x)
plt.plot(xx, yy, 'r', linewidth=1)       # 最终拟合的贝塞尔曲线
plt.scatter(xx[:], yy[:], 1, "blue")     #散点图,表示采样点
plt.show()
