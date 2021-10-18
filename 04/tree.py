import taichi as ti

ti.init()

gui = ti.GUI("tree", (400, 400))

r = 0.5
theta = 30

@ti.kernel
def getNextLeftPoint(p0:ti.Vector, theta0:ti.f32, r0:ti.f32) -> ti.Vector:
