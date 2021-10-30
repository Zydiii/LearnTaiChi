import taichi as ti
import handy_shader_functions as hsf

ti.init()

res_x = 960
res_y = 540
pixels = ti.Vector.field(3, ti.f32)
ti.root.dense(ti.i, res_x).dense(ti.j, res_y).place(pixels)

_PerlinPrecision = 8.0
_PerlinOctaves = 8.0
_PerlinSeed = 0.0

fg_cols = ti.Vector.field(4, ti.f32)
ti.root.dense(ti.i, 4).place(fg_cols)
fg_cols[0] = ti.Vector([0, 110, 202, 256]) / 256 # blue
fg_cols[1] = ti.Vector([232, 141, 122, 256]) / 256 # red
fg_cols[2] = ti.Vector([90, 188, 94, 256]) / 256 # green
fg_cols[3] = ti.Vector([161, 90, 188, 256]) / 256 # purple

bg_col = ti.Vector([229, 204, 175, 256]) / 256

@ti.func
def rnd(xy):
    return hsf.fract(ti.sin(xy.dot(ti.Vector([12.9898 - _PerlinSeed, 78.233+ _PerlinSeed]))) * (43758.5453 + _PerlinSeed))

@ti.func
def inter(a, b, x):
    f = (1.0 - ti.cos(x * 3.1415927)) * 0.5
    return a * (1.0 - f) + b *f

@ti.func
def perlin(uv):
    t = _PerlinPrecision
    p = 0.0

    for i in range(0, _PerlinOctaves):
        a = rnd(ti.Vector([ti.floor(t * uv.x) / t, ti.floor(t * uv.y) / t]))
        b = rnd(ti.Vector([ti.ceil(t * uv.x) / t, ti.floor(t * uv.y) / t]))
        c = rnd(ti.Vector([ti.floor(t * uv.x) / t, ti.ceil(t * uv.y) / t]))
        d = rnd(ti.Vector([ti.ceil(t * uv.x) / t, ti.ceil(t * uv.y) / t]))

        if ti.ceil(t * uv.x) / t == 1.0:
            b = rnd(ti.Vector([0.0, ti.floor(t*uv.y)/t]))
            d = rnd(ti.Vector([0.0, ti.ceil(t*uv.y) / t]));

        coef1 = hsf.fract(t*uv.x)
        coef2 = hsf.fract(t*uv.y)
        p += inter(inter(a,b,coef1), inter(c,d,coef1), coef2) * (1.0/pow(2.0,(i+0.6)))
        t *= 2.0

    return p

@ti.kernel
def render(t : ti.f32):
    for i, j in pixels:
        p = ti.Vector([i / res_x, j / res_y]) - 0.5
        p.x *= res_x / res_y
        r = p.norm()
        seed = ti.floor(t * 0.5)

        fg_col = ti.Vector([0.0, 0.0, 0.0, 0.0])
        fg_col += (ti.mod(seed, 4) == 0) * fg_cols[0]
        fg_col += (ti.mod(seed - 1, 4) == 0) * fg_cols[1]
        fg_col += (ti.mod(seed - 2, 4) == 0) * fg_cols[2]
        fg_col += (ti.mod(seed - 3, 4) == 0) * fg_cols[3]

        noise_scale = 0.15 + 0.075 * ti.mod(seed, 3)
        num_layers = 3 + 2 * ti.mod(seed, 5)
        seed *= num_layers

        v = 0.0
        for k in range(0, num_layers):
            h = noise_scale * perlin(p + ti.Vector([k + seed, k + seed])) + r
            if h < 0.4:
                v += 1.0 / num_layers

        fragColor = hsf.lerp(bg_col, fg_col, v)
        pixels[i, j] = ti.Vector([fragColor[0], fragColor[1], fragColor[2]])


result_dir = "./results"
video_manager = ti.VideoManager(output_dir=result_dir, framerate=24, automatic_build=False)

gui = ti.GUI("Canvas", res=(res_x, res_y))

for i in range(200):
    t = i * 0.01
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
