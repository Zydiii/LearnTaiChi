import taichi as ti
import random

@ti.data_oriented
class BezierBase:
    def __init__(self, N):
        # 阶数
        self.degree = N
        self.basePosNum = self.degree + 1
        self.t_num = 150 * self.degree
        # 基点坐标
        self.basePoint_pos = ti.Vector.field(2, dtype=ti.f32, shape=self.basePosNum)
        # 贝塞尔曲线坐标
        self.bezierCurve_pos = ti.Vector.field(2, dtype=ti.f32, shape=self.t_num)

    # 设置随机端点坐标
    @ti.kernel
    def setRandomBasePointPos(self):
        for i in range(0, self.basePosNum):
            self.basePoint_pos[i] = ti.Vector([ti.sqrt(ti.random()) * 0.9, ti.sqrt(ti.random()) * 0.8])
        self.sortBasePoint()

    # 按照 x 坐标排序，便于可视化
    @ti.func
    def sortBasePoint(self):
        for i in range(0, self.basePosNum):
            for j in range(0, self.basePosNum - i - 1):
                a1 = self.basePoint_pos[j]
                a2 = self.basePoint_pos[j + 1]
                if a1[0] > a2[0]:
                    self.basePoint_pos[j] = a2
                    self.basePoint_pos[j + 1] = a1


    # 计算贝塞尔曲线
    @ti.kernel
    def computeBezier(self, u:ti.i32):
        # p(u) = Σ^n_{k = 0} p_k C(n,k) u^k (1-u)^(n - k)
        uStep = u / self.t_num
        for k in range(0, self.degree + 1):
            self.bezierCurve_pos[u] += self.basePoint_pos[k] * self.computeBinomialCoeff(self.degree, k) * uStep ** k * (1 - uStep) ** (self.degree - k)

    @ti.func
    def computeBinomialCoeff(self, n:ti.i32, k:ti.i32):
        return self.computeFactorial(n) / (self.computeFactorial(k) * self.computeFactorial(n - k))

    @ti.func
    def computeFactorial(self, n):
        tmp = 1
        for i in range(1, n + 1):
            tmp *= i
        return tmp

    # 绘制基点
    def displayBasePoint(self, gui, radius=1, color=0x5e60d3):
        for i in range(0, self.degree):
            gui.line(self.basePoint_pos[i].to_numpy(), self.basePoint_pos[i + 1].to_numpy(), radius=radius, color=color)
        gui.circles(self.basePoint_pos.to_numpy(), radius=radius + 3, color=0xff6401)

    # 绘制曲线
    def displayMidPoint(self, gui, radius=1.5, color=0xffffff):
        gui.circles(self.bezierCurve_pos.to_numpy(), color=color, radius=radius)

