import taichi as ti
from BezierBase import BezierBase

@ti.kernel
def getSliderValue(x : ti.f32) -> ti.i32:
    return ti.cast(x, ti.i32)

if __name__ == "__main__":
    ti.init()
    # 迭代步长
    t = 0

    # ui控制参数
    done = False
    start = False

    # 绘制窗口
    width = 400
    height = 400
    gui = ti.GUI("Bezier Curve", (width, height))
    gui.button("Simulation On", event_name="startButton")
    degreeSetting = gui.slider("Set Degree", 1, 10, step=1)
    degreeSetting.value = 3

    # GUI
    while gui.running:
        gui.clear(0x83AF9B)

        # 交互响应
        if gui.get_event("startButton"):
            start = True
            done = False
            t = 0
            # 初始化
            degree = getSliderValue(degreeSetting.value)
            degreeSetting.value = degree
            bezierBase = BezierBase(degree)
            bezierBase.setRandomBasePointPos()

        # 计算并绘制贝塞尔曲线
        if start:
            # 绘制基点
            bezierBase.displayBasePoint(gui)
            if not done:
                if t < bezierBase.t_num:
                    bezierBase.computeBezier(t)
                    t += 1
                else:
                    done = True
            bezierBase.displayMidPoint(gui)
        gui.show()

