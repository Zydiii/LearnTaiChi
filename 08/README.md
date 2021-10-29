# 【作业五】 ShaderToy 的简单尝试

## 背景简介

首先找了一个非常简单但是看起来很炫的 ShaderToy Demo (来自 https://www.shadertoy.com/view/XsXXDn) 移植到了 Taichi 中实现

然后找了一个非常可爱的 ShaderToy Demo (来自 https://www.shadertoy.com/view/4t2SRh) 学习了一下它的实现原理，并且基于它的实现方式添加了垂直下落的雨滴

## 成功效果展示

![](../result/shaderTest.gif)

![](../result/umbrellar.gif)

## 整体结构

```
- testShader.py 参考 https://www.shadertoy.com/view/XsXXDn
- umbrellaShader.py 参考 https://www.shadertoy.com/view/4t2SRh
- handy_shader_functions.py 来自官方的工具类
```

## 运行方式

`python3 testShader.py`

`python3 umbrellaShader.py`