from waterColorBaseStructure import Poly
import taichi as ti
import handy_shader_functions as hsf

ti.init()
# cpu_max_num_threads = 1
res_x = 740
res_y = 540

pixels = ti.Vector.field(3, ti.f32)
ti.root.dense(ti.i, res_x).dense(ti.j, res_y).place(pixels)

@ti.kernel
def blend():
    for i, j in pixels:
        color = poly0.bg_col
        color = hsf.lerp(color, poly0.pixels[i, j], poly0.opacity)
        color = hsf.lerp(color, poly1.pixels[i, j], poly1.opacity)
        color = hsf.lerp(color, poly2.pixels[i, j], poly2.opacity)
        color = hsf.lerp(color, poly3.pixels[i, j], poly3.opacity)
        # color += hsf.lerp(poly0.pixels[i, j], poly1.pixels[i, j], 0.6)
        pixels[i, j] = color

if __name__ == "__main__":
    centerPos = ti.Vector([0.5, 0.5])
    radius = 0.2
    poly0 = Poly(30, centerPos, radius, res_x, res_y, 0.4)
    poly1 = Poly(40, centerPos, radius + 0.02, res_x, res_y, 0.4)
    poly2 = Poly(50, centerPos, radius + 0.04, res_x, res_y, 0.4)
    poly3 = Poly(60, centerPos, radius + 0.06, res_x, res_y, 0.4)

    # poly.getEdge()
    # poly.testIn(0.5, 0.5)

    gui = ti.GUI("Water Color", res=(res_x, res_y))

    while gui.running:
        for i in range(200):
            t = i * 0.05
            poly0.render(t)
            poly1.render(t)
            poly2.render(t)
            poly3.render(t)
            blend()
            gui.set_image(pixels)
            # poly.displayTest(gui)
            gui.show()