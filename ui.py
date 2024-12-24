# ui.py

import pygame
import pygame_gui
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COORDINATE_SYSTEM
from utils import draw_wave, draw_text, draw_coordinate_system
from save_load import save_settings, load_settings

class UI:
    def __init__(self, manager, waves, add_wave_callback, remove_wave_callback, coordinate_system):
        """
        初始化UI。

        :param manager: pygame_gui.UIManager实例
        :param waves: 波实例列表
        :param add_wave_callback: 添加波的回调函数
        :param remove_wave_callback: 移除波的回调函数
        :param coordinate_system: 初始坐标系模式 ("2D" 或 "3D")
        """
        self.manager = manager
        self.waves = waves
        self.add_wave_callback = add_wave_callback
        self.remove_wave_callback = remove_wave_callback
        self.coordinate_system = coordinate_system
        self.selected_wave = None if not waves else waves[0]

        # 创建UI元素
        self.create_ui()

    def create_ui(self):
        """
        创建UI组件。
        """
        # 波形选择下拉菜单
        self.waveform_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 20), (160, 30)),
            text="Waveform",
            manager=self.manager
        )
        self.waveform_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["Sine", "Cosine"],
            starting_option=self.selected_wave.waveform if self.selected_wave else "Sine",
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 50), (160, 30)),
            manager=self.manager
        )

        # 颜色选择下拉菜单
        self.color_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 90), (160, 30)),
            text="Color",
            manager=self.manager
        )
        self.color_options = ["Cyan", "Magenta", "Yellow", "Green", "Blue", "Red", "White"]
        self.color_mapping = {
            "Cyan": (0, 255, 255),
            "Magenta": (255, 0, 255),
            "Yellow": (255, 255, 0),
            "Green": (0, 255, 0),
            "Blue": (0, 0, 255),
            "Red": (255, 0, 0),
            "White": (255, 255, 255)
        }
        self.color_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.color_options,
            starting_option=self.get_color_option(),
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 120), (160, 30)),
            manager=self.manager
        )

        # 振幅滑动条
        self.amplitude_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 160), (160, 30)),
            text=f"Amplitude: {int(self.selected_wave.amplitude) if self.selected_wave else 50}",
            manager=self.manager
        )
        self.amplitude_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 190), (160, 20)),
            start_value=self.selected_wave.amplitude if self.selected_wave else 50,
            value_range=(10, 200),
            manager=self.manager
        )

        # 频率滑动条
        self.frequency_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 220), (160, 30)),
            text=f"Frequency: {self.selected_wave.frequency if self.selected_wave else 1}",
            manager=self.manager
        )
        self.frequency_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 250), (160, 20)),
            start_value=self.selected_wave.frequency if self.selected_wave else 1,
            value_range=(0.1, 5),
            manager=self.manager
        )

        # 速度滑动条
        self.speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 280), (160, 30)),
            text=f"Speed: {self.selected_wave.speed if self.selected_wave else 2}",
            manager=self.manager
        )
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 310), (160, 20)),
            start_value=self.selected_wave.speed if self.selected_wave else 2,
            value_range=(-10, 10),  # 增加速度范围
            manager=self.manager
        )

        # 保存和加载按钮
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 350), (75, 30)),
            text="Save",
            manager=self.manager
        )
        self.load_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 125, 350), (75, 30)),
            text="Load",
            manager=self.manager
        )

        # 添加和移除波按钮
        self.add_wave_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 400), (160, 30)),
            text="Add Wave",
            manager=self.manager
        )
        self.remove_wave_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 440), (160, 30)),
            text="Remove Wave",
            manager=self.manager
        )

        # 坐标系模式切换下拉菜单
        self.coordinate_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 480), (160, 30)),
            text="Coordinate System",
            manager=self.manager
        )
        self.coordinate_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["2D", "3D"],
            starting_option=self.coordinate_system,
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 510), (160, 30)),
            manager=self.manager
        )

        # 显示波函数和波动方程
        self.equation_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, 560), (360, 60)),
            text="Wave Equation: y(x, t) = A * sin(2πft - kx + φ)",
            manager=self.manager
        )

    def get_color_option(self):
        """
        根据选中波的颜色确定下拉菜单的初始选项。

        :return: 颜色名称字符串
        """
        if self.selected_wave:
            for name, value in self.color_mapping.items():
                if value == self.selected_wave.color:
                    return name
        return "White"

    def handle_event(self, event):
        """
        处理UI事件。

        :param event: Pygame事件
        """
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.save_button:
                save_settings(self.waves)
            elif event.ui_element == self.load_button:
                loaded_settings = load_settings()
                if loaded_settings:
                    self.waves.clear()
                    for wave_settings in loaded_settings:
                        wave = self.add_wave_callback(
                            origin=tuple(wave_settings["origin"]),
                            speed=wave_settings["speed"],
                            frequency=wave_settings["frequency"],
                            amplitude=wave_settings["amplitude"],
                            phase=wave_settings["phase"],
                            color=tuple(wave_settings["color"]),
                            waveform=wave_settings["waveform"]
                        )
                    if self.waves:
                        self.selected_wave = self.waves[0]
                        self.update_ui()
            elif event.ui_element == self.add_wave_button:
                new_wave = self.add_wave_callback(origin=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.selected_wave = new_wave
                self.update_ui()
            elif event.ui_element == self.remove_wave_button:
                self.remove_wave_callback()
                if self.waves:
                    self.selected_wave = self.waves[-1]
                else:
                    self.selected_wave = None
                self.update_ui()

        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.amplitude_slider and self.selected_wave:
                self.selected_wave.amplitude = event.value
                self.amplitude_label.set_text(f"Amplitude: {int(event.value)}")
            elif event.ui_element == self.frequency_slider and self.selected_wave:
                self.selected_wave.frequency = round(event.value, 2)
                self.frequency_label.set_text(f"Frequency: {self.selected_wave.frequency}")
            elif event.ui_element == self.speed_slider and self.selected_wave:
                self.selected_wave.speed = round(event.value, 2)
                self.speed_label.set_text(f"Speed: {self.selected_wave.speed}")

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.waveform_dropdown and self.selected_wave:
                self.selected_wave.waveform = event.text
            elif event.ui_element == self.color_dropdown and self.selected_wave:
                selected_color = event.text
                self.selected_wave.color = self.color_mapping.get(selected_color, (255, 255, 255))
            elif event.ui_element == self.coordinate_dropdown:
                self.coordinate_system = event.text

    def update_ui(self):
        """
        根据选中波的参数更新UI元素。
        """
        if self.selected_wave:
            self.waveform_dropdown.selected_option = self.selected_wave.waveform
            # 更新颜色下拉菜单
            for color_name, color_value in self.color_mapping.items():
                if color_value == self.selected_wave.color:
                    self.color_dropdown.selected_option = color_name
                    break
            self.amplitude_slider.set_current_value(self.selected_wave.amplitude)
            self.amplitude_label.set_text(f"Amplitude: {int(self.selected_wave.amplitude)}")
            self.frequency_slider.set_current_value(self.selected_wave.frequency)
            self.frequency_label.set_text(f"Frequency: {self.selected_wave.frequency}")
            self.speed_slider.set_current_value(self.selected_wave.speed)
            self.speed_label.set_text(f"Speed: {self.selected_wave.speed}")
        else:
            self.waveform_dropdown.selected_option = "Sine"
            self.color_dropdown.selected_option = "White"
            self.amplitude_slider.set_current_value(50)
            self.amplitude_label.set_text("Amplitude: 50")
            self.frequency_slider.set_current_value(1)
            self.frequency_label.set_text("Frequency: 1")
            self.speed_slider.set_current_value(2)
            self.speed_label.set_text("Speed: 2")

    def get_coordinate_system(self):
        """
        返回当前的坐标系模式。

        :return: "2D" 或 "3D"
        """
        return self.coordinate_system
