import taichi as ti
import numpy as np

ti.init()

x1 = 0.2
y1 = 0.2
x2 = 0.5
y2 = 0.5
x3 = 0.8
y3 = 0.1
dots_num = 1000
step = 10

my_gui = ti.GUI("Bezier", (800, 800))

# 基点
pos_base0 = ti.Vector.field(2, dtype = ti.f32, shape = 1)
pos_base1 = ti.Vector.field(2, dtype = ti.f32, shape = 1)
pos_base2 = ti.Vector.field(2, dtype = ti.f32, shape = 1)
# 计算中的线段端点
pos_mid0 = ti.Vector.field(2, dtype = ti.f32, shape = 1)
pos_mid1 = ti.Vector.field(2, dtype = ti.f32, shape = 1)

def displayBase():
    pos_base0 = ti.Vector([0.2, 0.2])
    pos_base1 = ti.Vector([0.5, 0.5])
    pos_base2 = ti.Vector([0.8, 0.1])
    my_gui.circle(pos_base0.to_numpy(), radius = 2, color=0x66ccff)
    my_gui.circle(pos_base1.to_numpy(), radius = 2, color=0x66ccff)
    my_gui.circle(pos_base2.to_numpy(), radius = 2, color=0x66ccff)
    my_gui.line(pos_base0.to_numpy(), pos_base1.to_numpy(), radius=1, color=0x66ccff)
    my_gui.line(pos_base1.to_numpy(), pos_base2.to_numpy(), radius=1, color=0x66ccff)

pos = ti.Vector.field(2, dtype = ti.f32, shape = dots_num)
xt = []
yt = []
x_dots12 = []
x_dots23 = []
y_dots12 = []
y_dots23 = []

# dots12 = ti.Vector.field(2, dtype = ti.f32, shape = dots_num)
# dots23 = ti.Vector.field(2, dtype = ti.f32, shape = dots_num)
# x1=-1, y1=1, x2=0, y2=-1, x3=1, y3=1, dots_num=1000

def two_degree_bc(i):  # bezier curve
    x_dots12 = np.linspace(x1, x2, dots_num)
    y_dots12 = np.linspace(y1, y2, dots_num)
    x_dots23 = np.linspace(x2, x3, dots_num)
    y_dots23 = np.linspace(y2, y3, dots_num)
    # for i in range(dots_num):
    x = x_dots12[i] + (x_dots23[i] - x_dots12[i]) * i / (dots_num - 1)
    y = y_dots12[i] + (y_dots23[i] - y_dots12[i]) * i / (dots_num - 1)
    xt.append(x)
    yt.append(y)
    pos[i] = ti.Vector([x, y])
    pos_mid0 = ti.Vector([x_dots12[i], y_dots12[i]])
    pos_mid1 = ti.Vector([x_dots23[i], y_dots23[i]])
    my_gui.circle(pos_mid0.to_numpy(), color=0xffffff, radius=1)
    my_gui.circle(pos_mid1.to_numpy(), color=0xffffff, radius=1)
    my_gui.line(pos_mid0.to_numpy(), pos_mid1.to_numpy(), color=0x007fff, radius=1)

if __name__ == "__main__":
    # two_degree_bc()
    my_gui.clear(0x112F41)
    i = 0
    j = 0
    while my_gui.running:
        displayBase()
        if i < step:
            i += 1
            if j < dots_num:
                two_degree_bc(j)
                my_gui.circles(pos.to_numpy(), color=0xffffff, radius=1)
                j += 1
            else:
                j = 0
                pos = ti.Vector.field(2, dtype = ti.f32, shape = dots_num)
            # my_gui.show()
        else:
            i = 0
        my_gui.show()

