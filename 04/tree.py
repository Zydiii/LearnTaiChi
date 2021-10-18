import taichi as ti

ti.init()

gui = ti.GUI("tree", (400, 400))

r = 0.5
theta = 30
num = 1
step = 1

pos = ti.Vector.field(2, ti.f32, num)
pos = ti.Vector([0.5, 0.1])
angle = ti.Vector.field(1, ti.f32, num)
angle = ti.Vector([90])

@ti.kernel
def run(num : ti.i32, theta : ti.f32, r : ti.f32, pos : ti.Vector.field, angle : ti.Vector.field):
    pos1 = ti.Vector.field(2, ti.f32, num)
    angle1 = ti.Vector.field(1, ti.f32, num)

    for i in pos:
        theta1 = angle[i] + theta
        theta2 = angle[i] - theta
        pos1[2*i] = ti.Vector([pos[i][0] + r * ti.sin(theta1), pos[i][1] + r * ti.sin(theta1)])
        pos1[2*i + 1] = ti.Vector([pos[i][0] + r * ti.sin(theta2), pos[i][1] + r * ti.sin(theta2)])
        angle1[2*i] = theta1
        angle1[2*i + 1] = theta2

gui = ti.GUI("tree", (400, 400))

while gui.running:
    if step > 0:
        run()
        r /= 2
        num *= 2
        step -= 1
    gui.show()
