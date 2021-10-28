import taichi as ti
import handy_shader_functions as hsf

ti.init()

res_x = 400
res_y = 400
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.kernel
def render(t : ti.f32):
    for i, j in pixels:
        color = ti.Vector([0.0, 0.0, 0.0])
        z = t
        l = 1.0
        for k in ti.static(range(3)):
            p = ti.Vector([float(i) / res_x, float(j) / res_y])
            uv = ti.Vector([p[0], p[1]])
            p -= 0.5
            p[0] *= (res_x / res_y)
            z += 0.07
            l = p.norm()
            uv += p / l * (ti.sin(z) + 1) * ti.abs(ti.sin(l * 9 - z- z))
            color[k] = 0.01 / (hsf.mod(uv, 1.5) - 0.5).norm()

        color /= l
        pixels[i,j] = color

gui = ti.GUI("Canvas", res=(res_x, res_y))

while gui.running:
    for i in range(100000):
        t = i * 0.03
        render(t)
        gui.set_image(pixels)
        gui.show()