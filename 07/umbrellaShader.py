import taichi as ti
import handy_shader_functions as hsf

ti.init()

res_x = 800
res_y = 450
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.func
def circle(center : ti.Vector, radius : ti.f32, coord : ti.Vector) -> ti.f32:
    offset = coord - center
    return ti.sqrt((offset.x * offset.x) + (offset.y * offset)) - radius

@ti.func
def render0(d : ti.f32, color : ti.Vector, stroke : ti.f32) -> ti.Vector:
    anti = d * 2.0
    strokeLayer = ti.Vector([0.05, 0.05, 0.05, 1.0 - hsf.smoothstep(-anti, anti, d - stroke)])
    colorLayer = ti.Vector([color, 1.0 - hsf.smoothstep(-anti, anti, d)])
    if stroke < 0.000001 :
        return colorLayer
    return ti.Vector(hsf.mix(strokeLayer.rgb, colorLayer.rgb, colorLayer.a), strokeLayer.a)

@ti.kernel
def render(t : ti.f32):
    for i, j in pixels:
        color = ti.Vector([0.0, 0.0, 0.0])
        z = t
        l = 1.0
        for k in ti.static(range(3)):
            p = ti.Vector([float(i) / res_x, float(j) / res_y])
            uv = p
            p -= 0.5
            p[0] *= (res_x / res_y)
            z += 0.07
            l = p.norm()
            uv += p / l * (ti.sin(z) + 1) * ti.abs(ti.sin(l * 9 - z- z))
            color[k] = 0.01 / (hsf.mod(uv, 1.1) - 0.5).norm()

        color /= l
        pixels[i,j] = color

# result_dir = "./results"
# video_manager = ti.VideoManager(output_dir=result_dir, framerate=24, automatic_build=False)

gui = ti.GUI("Canvas", res=(res_x, res_y))

for i in range(200):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()
    # pixels_img = pixels.to_numpy()
    # video_manager.write_frame(pixels_img)
    # print(f'\rFrame {i + 1}/200 is recorded', end='')

# print()
# print('Exporting .mp4 and .gif videos...')
# video_manager.make_video(gif=True, mp4=True)
# print(f'MP4 video is saved to {video_manager.get_output_filename(".mp4")}')
# print(f'GIF video is saved to {video_manager.get_output_filename(".gif")}')