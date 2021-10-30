from waterColorBaseStructure import Poly
import taichi as ti

ti.init(cpu_max_num_threads = 1)

res_x = 512
res_y = 512

if __name__ == "__main__":
    centerPos = ti.Vector([0.5, 0.5])
    radius = 0.5
    poly = Poly(4, centerPos, radius, res_x, res_y)

    gui = ti.GUI("Water Color", res=(res_x, res_y))
    while gui.running:
        for i in range(200):
            t = i * 0.01
            poly.render(t)
            poly.display(gui)
            gui.show()