from waterColorBaseStructure import Poly
import taichi as ti

ti.init(cpu_max_num_threads = 1)
# cpu_max_num_threads = 1
res_x = 960
res_y = 540

if __name__ == "__main__":
    centerPos = ti.Vector([0.5, 0.5])
    radius = 0.1
    poly = Poly(10, centerPos, radius, res_x, res_y)
    # poly.getEdge()
    # poly.testIn(0, 1)

    gui = ti.GUI("Water Color", res=(res_x, res_y))

    while gui.running:
        for i in range(200):
            t = i * 0.01
            poly.render(t)
            poly.display(gui)
            poly.displayTest(gui)
            gui.show()