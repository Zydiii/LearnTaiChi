import math
import taichi as ti
import handy_shader_functions as hsf

# 多边形，默认顶点顺序按照逆时针
@ti.data_oriented
class Poly():
    def __init__(self, N, centerPos, radius, res_x, res_y, opacity):
        # 顶点
        self.centerPos = centerPos
        self.radius = radius
        self.num = N
        self.vertices = ti.Vector.field(2, ti.f32)
        ti.root.dense(ti.i, self.num).place(self.vertices)
        self.generateVertices()
        self.warpVertex()
        # 边
        self.edgeNum = self.num
        self.edges = ti.Vector.field(2, ti.f32)
        ti.root.dense(ti.ij, (self.edgeNum, 2)).place(self.edges)
        self.edgeInfo = ti.Vector.field(2, ti.f32)
        ti.root.dense(ti.ij, (self.edgeNum, 2)).place(self.edgeInfo)
        self.generateEdge()
        self.generateEdgeInfo()
        # 显示相关
        self.res_x = res_x
        self.res_y = res_y
        self.pixels = ti.Vector.field(3, ti.f32)
        ti.root.dense(ti.i, self.res_x).dense(ti.j, self.res_y).place(self.pixels)
        # 激活的边及交点
        self.activeEdge = ti.field(ti.i32)
        ti.root.dense(ti.ij, (self.res_y, self.edgeNum)).place(self.activeEdge)
        self.activeInterX = ti.field(ti.f32)
        ti.root.dense(ti.ij, (self.res_y, self.edgeNum)).place(self.activeInterX)
        self.getActiveEdge()
        # 颜色
        self.bg_col = ti.Vector([229, 204, 175]) / 256
        self.fg_cols = ti.Vector.field(3, ti.f32)
        ti.root.dense(ti.i, 4).place(self.fg_cols)
        self.fg_cols[0] = ti.Vector([0, 110, 202]) / 256  # blue
        self.fg_cols[1] = ti.Vector([232, 141, 122]) / 256  # red
        self.fg_cols[2] = ti.Vector([90, 188, 94]) / 256  # green
        self.fg_cols[3] = ti.Vector([161, 90, 188]) / 256  # purple
        self.opacity = opacity

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

    # 歪曲顶点
    @ti.kernel
    def warpVertex(self):
        for i in range(0, self.num):
            strengh = 0.0
            if i == 0:
                strengh = (self.vertices[self.num - 1] - self.vertices[1]).norm()
            elif i == self.num - 1:
                strengh = (self.vertices[self.num - 2] - self.vertices[0]).norm()
            else:
                strengh = (self.vertices[i - 1] - self.vertices[i + 1]).norm()
            offset = ti.Vector([ti.random(), ti.random()]) - ti.Vector([0.6, 0.5])
            offset *= strengh
            self.vertices[i] += offset

    # 生成边的详细信息，没有处理边垂直的时候！！
    @ti.kernel
    def generateEdgeInfo(self):
        for i in range(0, self.edgeNum):
            highY = max(self.edges[i, 0].y, self.edges[i, 1].y)
            lowY = min(self.edges[i, 0].y, self.edges[i, 1].y)
            self.edgeInfo[i, 0] = ti.Vector([highY, lowY])
            # y = mx + b
            m = 0.00001
            if self.edges[i, 0].x != self.edges[i, 1].x :
                m = (self.edges[i, 0].y - self.edges[i, 1].y) / (self.edges[i, 0].x - self.edges[i, 1].x)
            b = self.edges[i, 0].y - self.edges[i, 0].x * m
            self.edgeInfo[i, 1] = ti.Vector([m, b])

    # 计算某个像素点从左到右穿过了多少条边，判断点是否在内部
    @ti.func
    def checkPixelIn(self, x, y):
        interCount = 0
        for j in range(0, self.edgeNum):
            if self.activeEdge[y, j] and self.activeInterX[y, j] < x:
                interCount += 1
        return interCount % 2

    # 获取会与扫描线相交的边和交点
    # 不同边的端点相等的时候扫描线可能会一个相等一个不等，好奇怪啊，感觉可能和精度有一点关系，但是可能影响不大，目前调不出来了。。。
    @ti.kernel
    def getActiveEdge(self):
        for i in range(0, self.res_y):
            y = i / self.res_y
            for j in range(0, self.edgeNum):
                if self.edgeInfo[j, 0].x >= y and self.edgeInfo[j, 0].y <= y:
                    self.activeEdge[i, j] = 1
                    self.activeInterX[i, j] = (y - self.edgeInfo[j, 1].y) / self.edgeInfo[j, 1].x
                else:
                    self.activeEdge[i, j] = 0

    # 计算像素点颜色
    @ti.kernel
    def render(self, t : ti.f32):
        seed = ti.floor(t * 0.5)
        index = ti.cast(ti.mod(seed, 4), ti.i32)
        fg_col = self.fg_cols[index]
        num_layers = 3 + 2 * ti.mod(seed, 5)
        for k in range(0, num_layers):
            seed *= num_layers
        for i, j in self.pixels:
            a = self.checkPixelIn(i / self.res_x, j)
            self.pixels[i, j] = hsf.lerp(self.bg_col, fg_col, a)

    # 显示
    def display(self, gui):
        gui.set_image(self.pixels)

    def displayTest(self, gui):
        for i in range(0, self.edgeNum):
            gui.line(self.edges[i, 0].to_numpy(), self.edges[i, 1].to_numpy())

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
            print(self.edgeInfo[i, 1])

    @ti.kernel
    def testIn(self, x:ti.f32, y:ti.f32):
        self.getActiveEdge()
        print("激活边")
        for i in self.activeEdge:
            print("i")
            print(i)
            print(self.activeEdge[i])
            print("交点")
            print(self.activeInterX[i])

        print("在")
        print(self.checkPixelIn(x))
