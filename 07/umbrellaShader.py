import taichi as ti
import handy_shader_functions as hsf

ti.init(cpu_max_num_threads=1)

res_x = 800
res_y = 450
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.func
def circle(center, radius, coord):
    offset = coord - center
    return ti.sqrt((offset.x * offset.x) + (offset.y * offset.y)) - radius

@ti.func
def ellipse(center, a, b, coord):
    a2 = a * a
    b2 = b * b
    return (b2 * (coord.x - center.x) * (coord.x - center.x) + a2 * (coord.y - center.y) * (coord.y - center.y) - a2 * b2) / (a2 * b2)

@ti.func
def line(p0, p1, width, coord):
    dir0 = p1 - p0
    dir1 = coord - p0
    h = hsf.clamp(dir0.dot(dir1) / dir0.dot(dir0), 0.0, 1.0)
    return (dir1 - dir0 * h).norm() - width * 0.5

@ti.func
def union(a : ti.f32, b : ti.f32):
    return ti.min(a, b)

@ti.func
def difference(a : ti.f32, b : ti.f32):
    return ti.max(a, -b)

@ti.func
def intersection(a : ti.f32, b : ti.f32):
    return ti.max(a, b)

@ti.func
def getColor(d, color):
    return ti.Vector([color[0], color[1], color[2], 1.0 - hsf.step(0, d)])

@ti.kernel
def render(t : ti.f32):
    for i, j in pixels:
        size = ti.min(res_x, res_y)
        uv = ti.Vector([i, j]) / res_x
        center = ti.Vector([0.5, 0.5 * res_y / res_x])

        # 伞柄
        bottom = 0.08
        handleWidth = 0.01
        handleRadius = 0.04
        d = circle(ti.Vector([0.5 - handleRadius + 0.5 * handleWidth, bottom]), handleRadius, uv)
        c = circle(ti.Vector([0.5 - handleRadius + 0.5 * handleWidth, bottom]), handleRadius - handleWidth, uv)
        d = difference(d, c)
        c = uv.y - bottom
        d = intersection(d, c)
        c = line(ti.Vector([0.5, center.y * 2.0 - 0.05]), ti.Vector([0.5, bottom]), handleWidth, uv)
        d = union(d, c)
        c = circle(ti.Vector([0.5, center.y * 2.0 - 0.05]), 0.01, uv)
        d = union(c, d)
        c = circle(ti.Vector([0.5 - handleRadius * 2.0 + handleWidth, bottom]), handleWidth * 0.5, uv)
        d = union(c, d)
        layer0 = getColor(d, ti.Vector([0.404, 0.298, 0.278]))

        # 伞身
        a = ellipse(ti.Vector([0.5, center.y * 2.0 - 0.34]), 0.25, 0.25, uv)
        b = ellipse(ti.Vector([0.5, center.y * 2 + 0.03]), 0.8, 0.35, uv)
        b = intersection(a, b)
        layer1 = getColor(b, ti.Vector([0.32, 0.56, 0.53]))

        # 伞花纹
        layer2 = ti.Vector([layer1[0], layer1[1], layer1[2], layer1[3]])
        sinuv = ti.Vector([uv.x, (ti.sin(uv.x * 40.0) * 0.02 + 1.0) * uv.y])
        r0 = 0.0
        r1 = 0.0
        r2 = 0.0
        e = 0.0
        f = 0.0
        for k in range(0, 10):
            time = hsf.mod(t + 0.3 * k, 3.0) * 0.2
            r1 = (time - 0.15) / 0.2 * 0.1 + 0.9
            r0 = (time - 0.15) / 0.2 * 0.9 + 0.1
            r2 = (time - 0.15) / 0.2 * 0.15 + 0.85
            e = ellipse(ti.Vector([0.5, center.y * 2.0 + 0.37 - time * r2]), 0.7 * r0, 0.35 * r1, sinuv)
            f = ellipse(ti.Vector([0.5, center.y * 2.0 + 0.41 - time]), 0.7 * r0, 0.35 * r1, sinuv)
            f = difference(e, f)
            f = intersection(f, b)
            layer = getColor(f, ti.Vector([1.0, 0.81, 0.27]))
            layer2 = hsf.mixFour(layer, layer2, layer[3])

        # 背景颜色
        p = ti.Vector([2 * i - res_x, 2 * j - res_y]) / ti.min(res_y, res_x)
        bgColor = ti.Vector([1.0, 0.8, 0.7 - 0.07 * p.y]) * (1 - 0.25 * p.norm())

        # 混合颜色
        color = ti.Vector([bgColor[0], bgColor[1], bgColor[2]])
        color = hsf.mixThree(ti.Vector([layer0[0], layer0[1], layer0[2]]), color, layer0[3])
        color = hsf.mixThree(ti.Vector([layer1[0], layer1[1], layer1[2]]), color, layer1[3])
        color = hsf.mixThree(ti.Vector([layer2[0], layer2[1], layer2[2]]), color, layer2[3])

        # 最终的颜色
        pixels[i,j] = ti.pow(color, ti.Vector([1.0 / 2.2, 1.0 / 2.2, 1.0 / 2.2]))

# result_dir = "./results"
# video_manager = ti.VideoManager(output_dir=result_dir, framerate=24, automatic_build=False)

gui = ti.GUI("Canvas", res=(res_x, res_y))

for i in range(300):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()
    # pixels_img = pixels.to_numpy()
    # video_manager.write_frame(pixels_img)
    # print(f'\rFrame {i + 1}/300 is recorded', end='')

# print()
# print('Exporting .mp4 and .gif videos...')
# video_manager.make_video(gif=True, mp4=True)
# print(f'MP4 video is saved to {video_manager.get_output_filename(".mp4")}')
# print(f'GIF video is saved to {video_manager.get_output_filename(".gif")}')