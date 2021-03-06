import taichi as ti
import handy_shader_functions as hsf

ti.init()

res_x = 800
res_y = 450
pixels = ti.Vector.field(3, ti.f32)
ti.root.dense(ti.i, res_x).dense(ti.j, res_y).place(pixels)

# 圆
@ti.func
def circle(center, radius, coord):
    offset = coord - center
    return ti.sqrt((offset.x * offset.x) + (offset.y * offset.y)) - radius

# 椭圆
@ti.func
def ellipse(center, a, b, coord):
    a2 = a * a
    b2 = b * b
    return (b2 * (coord.x - center.x) * (coord.x - center.x) + a2 * (coord.y - center.y) * (coord.y - center.y) - a2 * b2) / (a2 * b2)

# 线段
@ti.func
def line(p0, p1, width, coord):
    dir0 = p1 - p0
    dir1 = coord - p0
    h = hsf.clamp(dir0.dot(dir1) / dir0.dot(dir0), 0.0, 1.0)
    return (dir1 - dir0 * h).norm() - width * 0.5

@ti.func
def product(p1, p2, p3):
    return (p2.x-p1.x) * (p3.y-p1.y) - (p2.y-p1.y) * (p3.x-p1.x)

# 三角形
@ti.func
def triangle(a, b, c, coord):
    ret = 1
    if product(a, b, coord) > 0 and product(b, c, coord) > 0 and product(c, a, coord) > 0:
        ret = -1
    return ret

# 并集
@ti.func
def union(a : ti.f32, b : ti.f32):
    return ti.min(a, b)

# 差集
@ti.func
def difference(a : ti.f32, b : ti.f32):
    return ti.max(a, -b)

# 交集
@ti.func
def intersection(a : ti.f32, b : ti.f32):
    return ti.max(a, b)

# 根据距离场设定颜色
@ti.func
def getColor(d, color):
    return ti.Vector([color[0], color[1], color[2], 1.0 - hsf.step(0, d)])

@ti.kernel
def render(t : ti.f32):
    for i, j in pixels:
        uv = ti.Vector([i, j]) / res_x
        center = ti.Vector([0.5, 0.5 * res_y / res_x])
        p = ti.Vector([2 * i - res_x, 2 * j - res_y]) / ti.min(res_y, res_x)

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
            layer2 = hsf.lerp(layer2, layer, layer[3])

        # 雨滴
        layer3 = ti.Vector([0.0, 0.0, 0.0, 0.0])
        time = hsf.mod(t, 0.3)
        for m in range(0, 3):
            for k in range(0, 10):
                rainShape1 = ti.Vector([-0.01, -0.03])
                rainShape2 = ti.Vector([0.01, -0.03])
                p0 = ti.Vector([0.1 + k * 0.09, 0.55 - 0.2 * m - 5 * time * time])
                if p0.y < 0:
                    p0.y += 0.5
                p1 = p0 + rainShape1
                p2 = p0 + rainShape2
                e = triangle(p0, p1, p2, uv)
                rainCenter = p0 + ti.Vector([0, rainShape1.y])
                rainRadius = rainShape2.x
                f = circle(rainCenter, rainRadius, uv)
                f = union(e, f)
                layer = getColor(f, ti.Vector([0.2, 0.4, 0.6]))
                layer3 = hsf.lerp(layer3, layer, layer[3])

        # 背景颜色
        bgColor = ti.Vector([1.0, 0.8, 0.7 - 0.07 * p.y]) * (1 - 0.25 * p.norm())

        # 混合最终的颜色
        color = bgColor
        color = hsf.lerp(color, ti.Vector([layer0[0], layer0[1], layer0[2]]), layer0[3])
        color = hsf.lerp(color, ti.Vector([layer1[0], layer1[1], layer1[2]]), layer1[3])
        color = hsf.lerp(color, ti.Vector([layer2[0], layer2[1], layer2[2]]), layer2[3])
        color = hsf.lerp(color, ti.Vector([layer3[0], layer3[1], layer3[2]]), layer3[3])
        pixels[i,j] = ti.pow(color, ti.Vector([1.0 / 2.2, 1.0 / 2.2, 1.0 / 2.2]))

result_dir = "./results"
video_manager = ti.VideoManager(output_dir=result_dir, framerate=24, automatic_build=False)

gui = ti.GUI("Canvas", res=(res_x, res_y))

for i in range(200):
    t = i * 0.003
    render(t)
    gui.set_image(pixels)
    gui.show()
#     pixels_img = pixels.to_numpy()
#     video_manager.write_frame(pixels_img)
#     print(f'\rFrame {i + 1}/200 is recorded', end='')
#
# print()
# print('Exporting .mp4 and .gif videos...')
# video_manager.make_video(gif=True, mp4=True)
# print(f'MP4 video is saved to {video_manager.get_output_filename(".mp4")}')
# print(f'GIF video is saved to {video_manager.get_output_filename(".gif")}')
