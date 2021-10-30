import math
import taichi as ti
import handy_shader_functions as hsf

# 多边形，默认顶点顺序按照逆时针
@ti.data_oriented
class Poly():
    def __init__(self, N, centerPos, radius, res_x, res_y):
        # 顶点
        self.centerPos = centerPos
        self.radius = radius
        self.num = N
        self.vertices = ti.Vector.field(2, ti.f32)
        ti.root.dense(ti.i, self.num).place(self.vertices)
        self.generateVertices()
        # 边
        self.edgeNum = self.num
        self.edges = ti.Vector.field(2, ti.f32)
        ti.root.dense(ti.ij, (self.edgeNum, 2)).place(self.edges)
        self.generateEdge()
        # 边的详细信息
        self.edgeInfo = ti.Vector.field(2, ti.f32)
        ti.root.dense(ti.ij, (self.edgeNum, 2)).place(self.edgeInfo)
        self.generateEdgeInfo()
        # 激活的边及交点
        self.activeEdge = ti.field(ti.i32)
        ti.root.dense(ti.i, self.edgeNum).place(self.activeEdge)
        self.activeInterX = ti.field(ti.f32)
        ti.root.dense(ti.i, self.edgeNum).place(self.activeInterX)
        # 显示相关
        self.res_x = res_x
        self.res_y = res_y
        self.pixels = ti.Vector.field(3, ti.f32)
        ti.root.dense(ti.i, self.res_x).dense(ti.j, self.res_y).place(self.pixels)
        # 颜色
        self.bg_col = ti.Vector([229, 204, 175]) / 256
        self.fg_cols = ti.Vector.field(3, ti.f32)
        ti.root.dense(ti.i, 4).place(self.fg_cols)
        self.fg_cols[0] = ti.Vector([0, 110, 202]) / 256  # blue
        self.fg_cols[1] = ti.Vector([232, 141, 122]) / 256  # red
        self.fg_cols[2] = ti.Vector([90, 188, 94]) / 256  # green
        self.fg_cols[3] = ti.Vector([161, 90, 188]) / 256  # purple

    # 生成顶点
    @ti.kernel
    def generateVertices(self):
        interval = 2 * math.pi / self.num
        for i in self.vertices:
            angle = i * interval
            self.vertices[i] = self.centerPos + ti.Vector([self.radius * ti.sin(angle), self.radius * ti.cos(angle)])

    # 生成边信息
    @ti.kernel
    def generateEdge(self):
        for i in range(0, self.edgeNum - 1):
            self.edges[i, 0] = self.vertices[i]
            self.edges[i, 1] = self.vertices[i + 1]
        self.edges[self.edgeNum - 1, 0] = self.vertices[self.num - 1]
        self.edges[self.edgeNum - 1, 1] = self.vertices[0]

    @ti.kernel
    def getEdge(self):
        for i in range(0, self.edgeNum):
            print(i)
            print(self.edges[i, 0])
            print(self.edges[i, 1])

    @ti.kernel
    def getEdgeInfo(self):
        for i in range(0, self.edgeNum):
            print(i)
            print(self.edgeInfo[i, 0])

    # 生成边的详细信息
    @ti.kernel
    def generateEdgeInfo(self):
        for i in range(0, self.edgeNum):
            highY = max(self.edges[i, 0].y, self.edges[i, 1].y)
            lowY = min(self.edges[i, 0].y, self.edges[i, 1].y)
            # y = mx + b
            m = (self.edges[i, 0].y - self.edges[i, 1].y) / (self.edges[i, 0].x - self.edges[i, 1].x)
            b = self.edges[i, 0].y - self.edges[i, 0].x * m
            self.edgeInfo[i, 0] = ti.Vector([highY, lowY])
            self.edgeInfo[i, 1] = ti.Vector([m, b])

    # 计算某个像素点从左到右穿过了多少条边，判断点是否在内部
    @ti.func
    def checkPixelIn(self, x):
        interCount = 0
        for i in range(0, self.edgeNum):
            if self.activeEdge[i] and self.activeInterX[i] < x:
                interCount += 1
        return 1 - interCount % 2

    # 获取会与扫描线相交的边
    @ti.func
    def getActiveEdge(self, y):
        for i in range(0, self.edgeNum):
            if self.edgeInfo[i, 0].x >= y and self.edgeInfo[i, 0].y <= y:
                self.activeEdge[i] = 1
                self.activeInterX[i] = (y - self.edgeInfo[i, 1].y) / self.edgeInfo[i, 1].m
            else:
                self.activeEdge[i] = 0

    # 计算像素点颜色
    @ti.kernel
    def render(self, t : ti.f32):
        seed = ti.floor(t * 0.5)
        index = ti.cast(ti.mod(seed, 4), ti.i32)
        fg_col = self.fg_cols[index]
        for j in range(0, self.res_y):
            self.getActiveEdge(j / self.res_x)
            for i in range(0, self.res_x):
                a = self.checkPixelIn(i / self.res_x)
                self.pixels[i, j] = hsf.lerp(self.bg_col, fg_col, a)

    # 显示
    def display(self, gui):
        gui.set_image(self.pixels)