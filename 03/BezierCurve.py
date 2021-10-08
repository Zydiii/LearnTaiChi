import taichi as ti
import numpy as np

ti.init()

x1 = 1
y1 = 1
x2 = -1
y2 = -1
x3 = 0
y3 = 0
dots_num = 100
pos = ti.Vector.field(2, dtype = ti.f32, shape=(1,))

def two_degree_bc(x1=-1, y1=1, x2=0, y2=-1, x3=1, y3=1, dots_num=1000):  # bezier curve
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

if __name__ == "__main__":
    two_degree_bc()
    my_gui = ti.GUI("Bezier", (800, 800))
    while my_gui.running:
        for i in range(0, len(xt)):
            x = xt[i]
            y = xt[i]
            pos[0][0] = x
            pos[0][1] = y
            my_gui.circle(pos[0], color=0xffffff, radius=1)
        my_gui.show()
