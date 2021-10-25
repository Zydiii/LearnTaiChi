import taichi as ti

ti.init()

x = ti.field(ti.f32, shape=())
x1 = ti.field(ti.f32)
ti.root.place(x1)

y = ti.field(ti.f32, shape=3)
y1 = ti.field(ti.f32)
ti.root.dense(ti.i, 3).place(y1)

z = ti.field(ti.f32, shape=(3, 4))
z1 = ti.field(ti.f32)
ti.root.dense(ti.ij, (3, 4)).place(z1)

xx = ti.Matrix.field(2, 2, ti.f32, shape=5)
xx1 = ti.Matrix.field(2, 2, ti.f32)
ti.root.dense(ti.i, 5).place(xx1)

matrix = ti.field(ti.i32)
ti.root.dense(ti.ij, (2, 2)).dense(ti.ij, (2, 2)).place(matrix)

yy = ti.field(ti.i32)
ti.root.dense(ti.i, 5).dense(ti.j, 2).place(yy)

@ti.kernel
def fill():
    for i, j in yy:
        yy[i, j] = i*10 + j

# fill()
# print(yy[0, 0])

zz = ti.field(ti.i32)
block1 = ti.root.pointer(ti.i, 3)
block2 = block1.dense(ti.j, 3)
block2.place(zz)
# print(zz[0, 0])

l = ti.field(ti.i32)
block11 = ti.root.pointer(ti.i, 3)
block22 = block11.bitmasked(ti.j, 3)
block22.place(l)
# print(l[0, 0])

m = ti.field(ti.i32)
n = ti.field(ti.i32)
o = ti.field(ti.i32)
p1 = ti.root.pointer(ti.j, 3)
p2 = ti.root.pointer(ti.i, 2)
d11 = p1.dense(ti.i, 2)
d21 = p2.dense(ti.i, 2)
b22 = p2.bitmasked(ti.i, 2)
d11.place(m)
d21.place(n)
b22.place(o)
print(m[0, 0])

