import taichi as ti
from BezierBase import ThreeBezierBase

if __name__ == "__main__":
    ti.init()
    # 初始化
    threeBezierBase = ThreeBezierBase()
    pos_base0 = ti.Vector([0.2, 0.2])
    pos_base1 = ti.Vector([0.5, 0.5])
    pos_base2 = ti.Vector([0.8, 0.1])
    threeBezierBase.setBasePoint(pos_base0, pos_base1, pos_base2)
    threeBezierBase.getSubPoint()

    # 时间步长
    step = 10
    i = 0
    t = 0

    # GUI
    width = 500
    height = 500
    gui = ti.GUI("Bezier Curve", (width, height))
    while gui.running:
        gui.clear(0x112F41)
        threeBezierBase.displayBasePoint(gui)
        if i < step:
            if t < threeBezierBase.t_num:
                threeBezierBase.run(t)
                threeBezierBase.displayMidPoint(gui)
                gui.show()
                t += 1
            else:
                j = 0
            i += 1
        else:
            i = 0
