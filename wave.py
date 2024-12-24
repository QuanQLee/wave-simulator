# wave.py

import math
from settings import DEFAULT_WAVE_SPEED, DEFAULT_FREQUENCY, DEFAULT_AMPLITUDE

class Wave:
    def __init__(self, origin, speed=DEFAULT_WAVE_SPEED, frequency=DEFAULT_FREQUENCY,
                 amplitude=DEFAULT_AMPLITUDE, phase=0, color=(0, 255, 255), waveform="Sine"):
        """
        初始化一个Wave实例。

        :param origin: 波的起点 (x, y)
        :param speed: 波速
        :param frequency: 频率
        :param amplitude: 振幅
        :param phase: 相位
        :param color: 颜色
        :param waveform: 波形类型 ("Sine" 或 "Cosine")
        """
        self.origin = origin
        self.speed = speed
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        self.color = color
        self.waveform = waveform  # "Sine" 或 "Cosine"
        self.time = 0

    def update(self, dt):
        """
        更新波的时间。

        :param dt: 时间增量（秒）
        """
        self.time += dt

    def get_wave_value(self, distance):
        """
        根据距离和波形类型计算y值偏移。

        :param distance: 距离起点的距离
        :return: y值偏移
        """
        argument = 2 * math.pi * self.frequency * (distance - self.speed * self.time) / 100  # 距离缩放
        if self.waveform == "Sine":
            return math.sin(argument + self.phase)
        elif self.waveform == "Cosine":
            return math.cos(argument + self.phase)
        else:
            return math.sin(argument + self.phase)  # 默认正弦波

    def get_wave_points(self, width, height, coordinate_system="2D"):
        """
        生成波的点。

        :param width: 屏幕宽度
        :param height: 屏幕高度
        :param coordinate_system: 坐标系模式 ("2D" 或 "3D")
        :return: 点的列表 [(x, y), ...]
        """
        points = []
        for x in range(width):
            distance = x - self.origin[0]
            y_offset = self.amplitude * self.get_wave_value(distance)
            y = self.origin[1] + y_offset
            if coordinate_system == "2D":
                points.append((x, y))
            elif coordinate_system == "3D":
                # 简单的3D投影：Z轴深度影响Y轴缩放
                z = distance * 0.05  # 假设的Z轴值
                scale = max(0.1, 1 - abs(z) / width)  # 简单缩放因子
                y_3d = self.origin[1] + y_offset * scale
                points.append((x, y_3d))
        return points
