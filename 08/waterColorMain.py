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
        color = hsf.lerp(color, poly3.pixels[i, j], poly4.opacity)
        color = hsf.lerp(color, poly3.pixels[i, j], poly5.opacity)
        pixels[i, j] = color

@ti.kernel
def blur():
    for i, j in pixels:
        if i != 0 and j != 0 and i != poly0.res_x - 1 and j != poly0.res_y - 1:
            pixels[i, j] = (pixels[i - 1, j - 1] + pixels[i, j - 1] + pixels[i + 1, j - 1] +
                            pixels[i - 1, j] + pixels[i, j] + pixels[i + 1, j] +
                            pixels[i - 1, j + 1] + pixels[i, j + 1] + pixels[i + 1, j + 1]) / 9

result_dir = "./results"
video_manager = ti.VideoManager(output_dir=result_dir, framerate=24, automatic_build=False)

if __name__ == "__main__":
    centerPos = ti.Vector([0.5, 0.5])
    radius = 0.2
    poly0 = Poly(40, centerPos, radius, res_x, res_y, 0.4)
    poly1 = Poly(50, centerPos, radius + 0.01, res_x, res_y, 0.3)
    poly2 = Poly(50, centerPos, radius + 0.01, res_x, res_y, 0.2)
    poly3 = Poly(60, centerPos, radius + 0.02, res_x, res_y, 0.1)
    poly4 = Poly(60, centerPos, radius + 0.02, res_x, res_y, 0.1)
    poly5 = Poly(60, centerPos, radius + 0.04, res_x, res_y, 0.1)

    gui = ti.GUI("Water Color", res=(res_x, res_y))
    for i in range(200):
        t = i * 0.05
        poly0.render(t)
        poly1.render(t)
        poly2.render(t)
        poly3.render(t)
        poly4.render(t)
        poly5.render(t)
        if t != 0 and ti.mod(t, 4) == 0:
            poly0.helper()
            poly1.helper()
            poly2.helper()
            poly3.helper()
            poly4.helper()
            poly5.helper()
        blend()
        blur()
        gui.set_image(pixels)
        # poly.displayTest(gui)
        gui.show()
        pixels_img = pixels.to_numpy()
        video_manager.write_frame(pixels_img)
        print(f'\rFrame {i + 1}/200 is recorded', end='')

    print()
    print('Exporting .mp4 and .gif videos...')
    video_manager.make_video(gif=True, mp4=True)
    print(f'MP4 video is saved to {video_manager.get_output_filename(".mp4")}')
    print(f'GIF video is saved to {video_manager.get_output_filename(".gif")}')