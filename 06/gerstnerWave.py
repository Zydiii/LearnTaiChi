import taichi as ti

ti.init()

# Q = 0.5
# A = 0.1
# D = 1
# w = 20
# s = 0.5

res = 400

# 需要计算的点
particleNum = 1000
pos = ti.Vector.field(2, ti.f32)
ti.root.dense(ti.i, particleNum).place(pos)

# 多个波形叠加
WaveN = 4
Q = ti.field(ti.f32)
A = ti.field(ti.f32)
D = ti.field(ti.f32)
w = ti.field(ti.f32)
s = ti.field(ti.f32)
ti.root.dense(ti.i, WaveN).place(Q, A, D, w, s)

@ti.kernel
def getWave(t : ti.f32):
    for i in pos:
        pos[i] = getGerstner(i / particleNum, t)

@ti.func
def getGerstner(x : ti.f32, t : ti.f32) -> ti.Vector:
    ret = ti.Vector([0.0, 0.0])
    for i in range(0, WaveN):
        ret += ti.Vector([x + Q[i] * A[i] * D[i] * ti.cos(w[i] * D[i] * x + w[i] * s[i] * t), A[i] * ti.sin(w[i] * D[i] * x + s[i] * w[i] * t) + 0.1])
    return ret

@ti.kernel
def setWave():
    for i in Q:
        Q[i] = ti.sqrt(ti.random()) * (1 / WaveN)
        A[i] = ti.sqrt(ti.random()) * (0.5 / WaveN)
        D[i] = (ti.sqrt(ti.random()) - 0.5) * 2
        w[i] = ti.sqrt(ti.random()) * 40 + 30
        s[i] = ti.sqrt(ti.random()) * 0.1

# 时间
t = 0

setWave()

gui = ti.GUI("wave", res=(res, res))
axisXBegin = ti.Vector([0, 0.5])
axisXEnd = ti.Vector([1, 0.5])
axisYBegin = ti.Vector([0.5, 0])
axisYEnd = ti.Vector([0.5, 1])

while gui.running:
    gui.line(axisXBegin.to_numpy(), axisXEnd.to_numpy())
    gui.line(axisYBegin.to_numpy(), axisYEnd.to_numpy())
    getWave(t)
    t += 0.01
    gui.circles(pos.to_numpy(), radius=2)
    gui.show()
