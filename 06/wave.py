import taichi as ti

ti.init()

res = 400

# 需要计算的点
N = 1000
pos = ti.Vector.field(2, ti.f32)
ti.root.dense(ti.i, N).place(pos)

# 多个波形叠加
WaveN = 5
ratio = ti.field(ti.f32)
A = ti.field(ti.f32)
w = ti.field(ti.f32)
s = ti.field(ti.f32)
ti.root.dense(ti.i, WaveN).place(ratio, A, w, s)

# A = 0.3
# w = 20
# s = 0.1

# 时间
t = 0

@ti.kernel
def getWave(t : ti.f32):
    for i in pos:
        pos[i] = ti.Vector([i / N, getSin(i / N, t)])

@ti.func
def getSin(x : ti.f32, t : ti.f32) -> ti.f32:
    ret = 0.0
    for i in range(0, WaveN):
        ret += ratio[i] * (A[i] * ti.sin(w[i] * (x - 0.5) + t * s[i] * w[i]) + 0.5)
    return ret

@ti.kernel
def setWave():
    for i in ratio:
        ratio[i] = ti.sqrt(ti.random()) * (1.5 / WaveN)
        A[i] = ti.sqrt(ti.random()) * (2 / WaveN)
        w[i] = ti.sqrt(ti.random()) * 20 + 20
        s[i] = ti.sqrt(ti.random()) * 0.5

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
