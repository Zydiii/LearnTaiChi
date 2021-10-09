import taichi as ti
from BezierBase import ThreeBezierBase

def clickButton():
    print("text")

if __name__ == "__main__":
    ti.init()
    # 初始化
    threeBezierBase = ThreeBezierBase(5)
    threeBezierBase.setRandomBasePointPos()

    # 时间步长
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
            if not done:
                if t < threeBezierBase.t_num:
                    threeBezierBase.computeBezier(t)
                    t += 1
                else:
                    done = True
            threeBezierBase.displayMidPoint(gui)
            gui.show()
        else:
            gui.show()

