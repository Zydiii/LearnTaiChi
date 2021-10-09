import taichi as ti
from BezierBase import ThreeBezierBase

def clickButton():
    print("text")

if __name__ == "__main__":
    ti.init()
    # 初始化
    threeBezierBase = ThreeBezierBase()
    pos_base0 = ti.Vector([0.2, 0.2])
    pos_base1 = ti.Vector([0.5, 0.5])
    pos_base2 = ti.Vector([0.8, 0.1])
    threeBezierBase.setBasePoint(pos_base0, pos_base1, pos_base2)

    # 时间步长
    step = 10
    substep = 0
    t = 0

    # ui控制参数
    done = False
    start = False

    # GUI
    width = 500
    height = 500
    gui = ti.GUI("Bezier Curve", (width, height))
    gui.button("Start", event_name="clickButton")
    while gui.running:
        gui.clear(0x112F41)
        # GUI
        threeBezierBase.displayBasePoint(gui)

        # 交互响应
        if gui.get_event("clickButton"):
            start = True

        # 计算并绘制贝塞尔曲线
        if start:
            if done:
                threeBezierBase.displayMidPoint(gui)
                gui.show()
            else:
                if substep < step:
                    if t < threeBezierBase.t_num:
                        threeBezierBase.run(t)
                        threeBezierBase.displayMidPoint(gui)
                        t += 1
                        substep += 1
                        gui.show()
                    else:
                        done = True
                    #     t = 0
                    # substep += 1
                else:
                    substep = 0
        else:
            gui.show()

