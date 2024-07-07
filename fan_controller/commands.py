capabilites = [
    {"command": "off", "description": "Turn fan off"},
    {"command": "fan_1", "description": "Turn fan on power level 1"},
    {"command": "fan_2", "description": "Turn fan on power level 2"},
    {"command": "fan_3", "description": "Turn fan on power level 3"},
    {"command": "fan_4", "description": "Turn fan on power level 4"},
    {"command": "fan_5", "description": "Turn fan on power level 5"},
    {"command": "fan_6", "description": "Turn fan on power level 6"},
    # {"command": "light_on", "description": "Turn light on"},
    # {"command": "low", "description": ""},
    # {"command": "high", "description": ""},
    # {"command": "timer_setting_1", "description": ""},
    # {"command": "timer_setting_2", "description": ""},
    # {"command": "timer_setting_3", "description": ""}
]

commands = {
    "off": {"decimal": 9912297, "binary": 0b100101110011111111101001},
    "light_on": {"decimal": 9912299, "binary": 0b100101110011111111101011},
    "fan_1": {"decimal": 9912061, "binary": 0b100101110011111011111101},
    "fan_2": {"decimal": 9912189, "binary": 0b100101110011111101111101},
    "fan_3": {"decimal": 9911933, "binary": 0b100101110011111001111101},
    "fan_4": {"decimal": 9912253, "binary": 0b100101110011111110111101},
    "fan_5": {"decimal": 9911997, "binary": 0b100101110011111010111101},
    "fan_6": {"decimal": 9912125, "binary": 0b100101110011111100111101},
    "low": {"decimal": 9912203, "binary": 0b100101110011111110001011},
    "high": {"decimal": 9912139, "binary": 0b100101110011111101001011},
    "timer_setting_1": {"decimal": 9912037, "binary": 0b100101110011111011100101},
    "timer_setting_2": {"decimal": 9911909, "binary": 0b100101110011111001100101},
    "timer_setting_3": {"decimal": 9912101, "binary": 0b100101110011111100100101},
}


def registration(device_name):
    """Generate registration message to server"""
    message = {"name": device_name, "capabilities": capabilites}
    return message


class Command:
    protocol = 6

    def __init__(self) -> None:
        self.decimal = 0
        self.binary = 0
