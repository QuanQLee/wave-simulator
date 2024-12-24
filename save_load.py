# save_load.py

import json
from settings import SETTINGS_FILE

def save_settings(waves):
    """
    将当前波的设置保存到JSON文件。

    :param waves: 波实例列表
    """
    settings = []
    for wave in waves:
        wave_settings = {
            "origin": wave.origin,
            "speed": wave.speed,
            "frequency": wave.frequency,
            "amplitude": wave.amplitude,
            "phase": wave.phase,
            "color": wave.color,
            "waveform": wave.waveform
        }
        settings.append(wave_settings)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_settings():
    """
    从JSON文件加载波的设置。

    :return: 波设置列表或None
    """
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        return None
