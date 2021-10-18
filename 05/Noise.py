import taichi as ti

ti.init()
res = 400

# 59.21~60 FPS
pixels = ti.field(ti.f32, (res, res))

# dense structure
# pixels = ti.field(ti.f32)
# 59.97~60 FPS
# ti.root.dense(ti.ij, (res, res)).place(pixels)
# 59.97~60 FPS
# ti.root.dense(ti.i, res).dense(ti.j, res).place(pixels)
# 59.84~60 FPS
# ti.root.dense(ti.j, res).dense(ti.i, res).place(pixels)

# sparse structure
# pixels = ti.field(ti.f32)
# ti.root.pointer(ti.ij, (200, 200)).dense(ti.ij, (2, 2)).place(pixels)




@ti.func
def fract(x):
    return x - ti.floor(x)

@ti.func
def lerp(x, y, w):
    return (y - x) * (3.0 - w * 2.0) * w * w + x

@ti.func
def dot(l, r):
    return l.dot(r)

# https://www.shadertoy.com/view/Xsl3Dl
@ti.func
def hash_3d(p):
    p = ti.Vector([
        p.dot(ti.Vector([127.1, 311.7, 74.7])),
        p.dot(ti.Vector([269.5, 183.3, 246.1])),
        p.dot(ti.Vector([113.5, 271.9, 124.6]))
    ])
    return -1 + 2 * fract(ti.sin(p) * 43758.5453123)

@ti.func
def gradient_noise_3d(p):
    i = ti.floor(p)
    f = fract(p)

    u = f * f * (3.0 - 2.0 * f)

    return lerp(lerp(lerp(dot(hash_3d(i + ti.Vector([0.0, 0.0, 0.0])), f - ti.Vector([0.0, 0.0, 0.0])),
                          dot(hash_3d(i + ti.Vector([1.0, 0.0, 0.0])), f - ti.Vector([1.0, 0.0, 0.0])), u.x),
                     lerp(dot(hash_3d(i + ti.Vector([0.0, 1.0, 0.0])), f - ti.Vector([0.0, 1.0, 0.0])),
                          dot(hash_3d(i + ti.Vector([1.0, 1.0, 0.0])), f - ti.Vector([1.0, 1.0, 0.0])), u.x), u.y),
                lerp(lerp(dot(hash_3d(i + ti.Vector([0.0, 0.0, 1.0])), f - ti.Vector([0.0, 0.0, 1.0])),
                          dot(hash_3d(i + ti.Vector([1.0, 0.0, 1.0])), f - ti.Vector([1.0, 0.0, 1.0])), u.x),
                     lerp(dot(hash_3d(i + ti.Vector([0.0, 1.0, 1.0])), f - ti.Vector([0.0, 1.0, 1.0])),
                          dot(hash_3d(i + ti.Vector([1.0, 1.0, 1.0])), f - ti.Vector([1.0, 1.0, 1.0])), u.x), u.y), u.z)

@ti.kernel
def paint(z: ti.f32):
    for P in ti.grouped(pixels):
        fp = P * 0.01
        p = ti.Vector([fp.x, fp.y, z])
        pixels[P] = gradient_noise_3d(p) * 0.5 + 0.5

gui = ti.GUI("Perlin Noise", res=(res, res))

step = 0.0
while True:
    paint(step)
    step += 0.01
    gui.set_image(pixels)
    gui.show()

    # ti.print_profile_info()
    # ti.print_kernel_profile_info()