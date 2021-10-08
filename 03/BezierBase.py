import taichi as ti
import numpy as np

@ti.data_oriented
class ThreeBezierBase:
    def __init__(self):
        # 基点坐标
        self.pos_base0 = ti.Vector.field(2, dtype=ti.f32, shape=1)
        self.pos_base1 = ti.Vector.field(2, dtype=ti.f32, shape=1)
        self.pos_base2 = ti.Vector.field(2, dtype=ti.f32, shape=1)
        # 计算步长
        self.t_num = 500
        # 根据步长插值的端点坐标
        self.pos_sub0 = ti.Vector.field(2, dtype=ti.f32, shape=self.t_num)
        self.pos_sub1 = ti.Vector.field(2, dtype=ti.f32, shape=self.t_num)
        # 某一步长中端点坐标
        self.pos_mid0 = ti.Vector.field(2, dtype=ti.f32, shape=1)
        self.pos_mid1 = ti.Vector.field(2, dtype=ti.f32, shape=1)
        # 贝塞尔曲线坐标
        self.pos = ti.Vector.field(2, dtype=ti.f32, shape=self.t_num)

    # 设置端点坐标
    def setBasePoint(self, p1 : ti.template, p2 : ti.template, p3 : ti.template):
        self.pos_base0 = p1
        self.pos_base1 = p2
        self.pos_base2 = p3
        self.getSubPoint()

    # 绘制基点
    def displayBasePoint(self, gui, radius=2, color=0x66ccff):
        gui.circle(self.pos_base0.to_numpy(), radius=radius + 1, color=color)
        gui.circle(self.pos_base1.to_numpy(), radius=radius + 1, color=color)
        gui.circle(self.pos_base2.to_numpy(), radius=radius + 1, color=color)
        gui.line(self.pos_base0.to_numpy(), self.pos_base1.to_numpy(), radius=1, color=color)
        gui.line(self.pos_base1.to_numpy(), self.pos_base2.to_numpy(), radius=1, color=color)

    # 计算插值后的端点
    @ti.kernel
    def getSubPoint(self):
        step0 = (self.pos_base1 - self.pos_base0) / self.t_num
        step1 = (self.pos_base2 - self.pos_base1) / self.t_num
        for i in range(0, self.t_num):
            self.pos_sub0[i] = self.pos_base0 + step0 * i
            self.pos_sub1[i] = self.pos_base1 + step1 * i

    # 计算
    @ti.kernel
    def run(self, t : ti.i32):
        self.pos_mid0[0] = ti.Vector([self.pos_sub0[t][0], self.pos_sub0[t][1]])
        self.pos_mid1[0] = ti.Vector([self.pos_sub1[t][0], self.pos_sub1[t][1]])
        midPoint = self.pos_mid0[0] + (self.pos_mid1[0] - self.pos_mid0[0]) * t / (self.t_num - 1)
        self.pos[t] = midPoint

    # 绘制中途的端点
    def displayMidPoint(self, gui, radius=1, color=0x007fff):
        gui.circles(self.pos.to_numpy(), color=0xffffff, radius=1)
        gui.circle(self.pos_mid0[0].to_numpy(), color=color, radius=radius+1)
        gui.circle(self.pos_mid1[0].to_numpy(), color=color, radius=radius+1)
        gui.line(self.pos_mid0[0].to_numpy(), self.pos_mid1[0].to_numpy(), color=color, radius=radius)

