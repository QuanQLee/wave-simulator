# main.py

import pygame
import sys
import math
import settings  # 导入settings.py
from wave import Wave
from ui import UI
from utils import draw_wave, draw_text, draw_coordinate_system
from save_load import save_settings, load_settings

def main():
    pygame.init()
    pygame.display.set_caption("Wave Simulator")

    # 设置窗口图标
    try:
        logo = pygame.image.load(settings.LOGO_PATH)
        pygame.display.set_icon(logo)
    except pygame.error:
        print("Failed to load logo image. Make sure 'assets/logo.png' exists.")

    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    # 初始化pygame_gui管理器
    import pygame_gui
    manager = pygame_gui.UIManager((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    # 创建初始波实例
    waves = []
    # 波源1：正弦波
    wave1 = Wave(origin=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2),
                 color=(0, 255, 255), waveform="Sine")
    waves.append(wave1)
    # 波源2：余弦波，反相位
    wave2 = Wave(origin=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2),
                 speed=4, frequency=1, amplitude=50,
                 phase=math.pi, color=(255, 255, 255), waveform="Cosine")
    waves.append(wave2)

    # 添加和移除波的回调函数
    def add_wave_callback(origin=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2),
                         speed=2, frequency=1, amplitude=50,
                         phase=0, color=(255, 255, 255), waveform="Sine"):
        new_wave = Wave(origin=origin, speed=speed, frequency=frequency,
                        amplitude=amplitude, phase=phase, color=color, waveform=waveform)
        waves.append(new_wave)
        return new_wave

    def remove_wave_callback():
        if waves:
            waves.pop()

    # 创建UI实例
    ui = UI(manager, waves, add_wave_callback, remove_wave_callback, settings.COORDINATE_SYSTEM)

    running = True
    while running:
        time_delta = clock.tick(settings.FPS) / 1000.0  # 时间增量（秒）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)
            ui.handle_event(event)

        manager.update(time_delta)

        # 更新波
        for wave in waves:
            wave.update(time_delta)

        # 获取当前坐标系模式
        coordinate_system = ui.get_coordinate_system()

        # 清屏
        screen.fill(settings.BACKGROUND_COLOR)

        # 绘制坐标系
        font = pygame.font.SysFont(None, 24)
        draw_coordinate_system(screen, font, settings)

        # 计算叠加波（叠加）
        combined_wave = []
        for x in range(settings.SCREEN_WIDTH):
            y = settings.SCREEN_HEIGHT // 2
            for wave in waves:
                distance = x - wave.origin[0]
                y += wave.amplitude * wave.get_wave_value(distance)
            if coordinate_system == "2D":
                combined_wave.append((x, y))
            elif coordinate_system == "3D":
                # 简单的3D投影：Z轴深度影响Y轴缩放
                z = (x - settings.SCREEN_WIDTH//2) * 0.05  # 假设的Z轴值
                scale = max(0.1, 1 - abs(z)/settings.SCREEN_WIDTH)
                y_3d = settings.SCREEN_HEIGHT // 2 + (y - settings.SCREEN_HEIGHT//2) * scale
                combined_wave.append((x, y_3d))

        # 绘制叠加波
        pygame.draw.lines(screen, (255, 255, 255), False, combined_wave, 2)

        # 可选：绘制单独的波
        for wave in waves:
            points = wave.get_wave_points(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, coordinate_system)
            draw_wave(screen, points, wave.color)

        # 绘制UI
        manager.draw_ui(screen)

        # 显示波函数和波动方程
        equation_text = "Wave Equation: y(x, t) = A * sin(2πft - kx + φ)" if waves else ""
        draw_text(screen, equation_text, (20, 620), font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
