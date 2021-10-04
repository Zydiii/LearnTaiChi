import taichi as ti

ti.init(ti.cpu)

# gravitational constant 6.67408e-11, using 1 for simplicity
G = 1
PI = 3.141592653

# number of planets
N = 1000
# unit mass
m = 5
# galaxy size
galaxy_size = 0.4
# planet radius (for rendering)
planet_radius = 2
# init vel
init_vel = 120

# time-step size
h = 1e-5
# substepping
substepping = 10

# 鼠标左键是否按下标识
leftmousePressed = False
# 虚拟的质量
mouse_m = 10000

# pos, vel and force of the planets
# Nx2 vectors
mouse_pos = ti.Vector.field(2, ti.f32, shape=())
pos = ti.Vector.field(2, ti.f32, N)
vel = ti.Vector.field(2, ti.f32, N)
force = ti.Vector.field(2, ti.f32, N)

@ti.kernel
def initialize():
    center=ti.Vector([0.5, 0.5])
    for i in range(N):
        theta = ti.random() * 2 * PI
        r = (ti.sqrt(ti.random()) * 0.7 + 0.3) * galaxy_size
        offset = r * ti.Vector([ti.cos(theta), ti.sin(theta)])
        pos[i] = center+offset
        vel[i] = [-offset.y, offset.x]
        vel[i] *= init_vel

@ti.kernel
def compute_force():
    # clear force
    for i in range(N):
        force[i] = ti.Vector([0.0, 0.0])
    # compute gravitational force
    for i in range(N):
        p = pos[i]
        for j in range(i): # bad memory footprint and load balance, but better CPU performance
            diff = p-pos[j]
            # print(diff)
            r = diff.norm(1e-5)
            # gravitational force -(GMm / r^2) * (diff/r) for i
            f = -G * m * m * (1.0/r)**3 * diff
            # assign to each particle
            force[i] += f
            force[j] += -f

@ti.kernel
def compute_force_mouse():
    # clear force
    for i in range(N):
        force[i] = ti.Vector([0.0, 0.0])
    # compute gravitational force
    for i in range(N):
        p = pos[i]
        diff = mouse_pos[None] - p
        r = diff.norm(1e-5)
        # gravitational force -(GMm / r^2) * (diff/r) for i
        f = G * m * mouse_m * (1.0 / r) ** 3 * diff
        # assign to each particle
        force[i] += f

@ti.kernel
def update():
    dt = h/substepping
    for i in range(N):
        #symplectic euler
        vel[i] += dt*force[i]/m
        pos[i] += dt*vel[i]

gui = ti.GUI('N-body problem', (512, 512))

initialize()
while gui.running:
    # 如果鼠标没有按下，检测按下信号
    if not leftmousePressed:
        if (gui.get_event(ti.GUI.PRESS, ti.GUI.LMB)):
            leftmousePressed = True
    # 如果鼠标按下，检测鼠标位置和释放信号
    if leftmousePressed:
        mouse_pos[None] = gui.get_cursor_pos()
        if (gui.get_event(ti.GUI.RELEASE, ti.GUI.SPACE)):
            leftmousePressed = False
    for i in range(substepping):
        if(leftmousePressed):
            compute_force_mouse()
            update()
        compute_force()
        update()

    gui.clear(0x112F41)
    gui.circles(pos.to_numpy(), color=0xffffff, radius=planet_radius)
    gui.show()
