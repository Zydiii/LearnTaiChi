import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


x1 = 10
y1 = 80
x2 = 50
y2 = 10
x3 = 90
y3 = 80
dots_num = 100


def two_degree_bc(x1=10, y1=80, x2=50, y2=10, x3=90, y3=80, dots_num=100):  # bezier curve
    global xt, yt, x_dots12, x_dots23, y_dots12, y_dots23
    xt = []
    yt = []
    x_dots12 = np.linspace(x1, x2, dots_num)
    y_dots12 = np.linspace(y1, y2, dots_num)
    x_dots23 = np.linspace(x2, x3, dots_num)
    y_dots23 = np.linspace(y2, y3, dots_num)
    for i in range(dots_num):
        x = x_dots12[i] + (x_dots23[i] - x_dots12[i]) * i / (dots_num - 1)
        y = y_dots12[i] + (y_dots23[i] - y_dots12[i]) * i / (dots_num - 1)
        xt.append(x)
        yt.append(y)


def run(i):
    art1.set_data(x_dots12[i], y_dots12[i])
    art2.set_data(x_dots23[i], y_dots23[i])
    art3.set_data([x_dots12[i], x_dots23[i]], [y_dots12[i], y_dots23[i]])
    art4.set_data(xt[i], yt[i])
    return art1, art2, art3, art4


two_degree_bc()
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect(1)
plt.xlim([0, 100])
plt.ylim([0, 100])
ax.plot([x1, x2], [y1, y2], color='#3e82fc')
ax.plot([x2, x3], [y2, y3], color='#3e82fc')
ax.plot(xt, yt, color='orange')
art1, = ax.plot(x_dots12[0], y_dots12[0], color='green', marker='o')  # scatter得到的对象不是一个list，是一个object
art2, = ax.plot(x_dots23[0], y_dots23[0], color='green', marker='o')
art3, = ax.plot([x_dots12[0], x_dots23[0]], [y_dots12[0], y_dots23[0]],
                color='purple')  # plot得到的结果是一个list，只包含一个元素，即一个形状object
art4, = ax.plot(xt[0], yt[0], color='red', marker='o')

ani = animation.FuncAnimation(
    fig, run, frames=range(100), interval=2, blit=True, save_count=50)
plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def B_nx(n, i, x):
#     if i > n:
#         return 0
#     elif i == 0:
#         return (1-x)**n
#     elif i == 1:
#         return n*x*((1-x)**(n-1))
#     return B_nx(n-1, i, x)*(1-x)+B_nx(n-1, i-1, x)*x
#
# def get_value(p, canshu):
#     sumx = 0.
#     sumy = 0.
#     length = len(p)-1
#     for i in range(0, len(p)):
#         sumx += (B_nx(length, i, canshu) * p[i][0])
#         sumy += (B_nx(length, i, canshu) * p[i][1])
#     return sumx, sumy
#
# def get_newxy(p,x):
#     xx = [0] * len(x)
#     yy = [0] * len(x)
#     for i in range(0, len(x)):
#         print('x[i]=', x[i])
#         a, b = get_value(p, x[i])
#         xx[i] = a
#         yy[i] = b
#         print('xx[i]=', xx[i])
#     return xx, yy
#
# p = np.array([                           #控制点，控制贝塞尔曲线的阶数n
#     [2, -4],
#     [3, 8],
#     [5, 1],
#     [7, 6],
#     [9, 4],
#     [7, 1],
# ])
#
# x = np.linspace(0, 1, 101)
# xx, yy = get_newxy(p, x)
# plt.plot(xx, yy, 'r', linewidth=1)       # 最终拟合的贝塞尔曲线
# plt.scatter(xx[:], yy[:], 1, "blue")     #散点图,表示采样点
# plt.show()
