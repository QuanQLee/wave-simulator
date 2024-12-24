# utils.py

import pygame

def draw_wave(screen, points, color):
    """
    在屏幕上绘制波。

    :param screen: Pygame屏幕表面
    :param points: 点的列表 [(x, y), ...]
    :param color: 波的颜色
    """
    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, 2)

def draw_text(screen, text, position, font, color=(255, 255, 255)):
    """
    在屏幕上渲染并绘制文本。

    :param screen: Pygame屏幕表面
    :param text: 要显示的文本
    :param position: 文本位置 (x, y)
    :param font: Pygame字体对象
    :param color: 文本颜色
    """
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_coordinate_system(screen, font, settings):
    """
    在屏幕上绘制坐标系。

    :param screen: Pygame屏幕表面
    :param font: Pygame字体对象
    :param settings: settings.py 中的设置。
    """
    width, height = screen.get_size()
    axis_color = (200, 200, 200)
    # X轴
    pygame.draw.line(screen, axis_color, (0, height // 2), (width, height // 2), 2)
    # Y轴
    pygame.draw.line(screen, axis_color, (width // 2, 0), (width // 2, height), 2)
    # 标签
    draw_text(screen, "X", (width - 20, height // 2 - 10), font)
    draw_text(screen, "Y", (width // 2 + 10, 10), font)
