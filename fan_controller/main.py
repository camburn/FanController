import time

import machine
import mip
import network
import ujson
import urequests
from rpi_rf import RFDevice

RADIO_TX_PIN = 13

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
    #Computer Room
    "off": {"decimal": 11526121, "binary": 0b101011111101111111101001 },
    "light_on": {"decimal": None, "binary": None},
    "fan_1": {"decimal": 11525885, "binary": 0b101011111101111011111101 },
    "fan_2": {"decimal": 11526013, "binary": 0b101011111101111101111101 },
    "fan_3": {"decimal": 11525757, "binary": 0b101011111101111001111101 },
    "fan_4": {"decimal": 11526077, "binary": 0b101011111101111110111101 },
    "fan_5": {"decimal": 11525821, "binary": 0b101011111101111010111101 },
    "fan_6": {"decimal": 11525949, "binary": 0b101011111101111100111101 },
    "low": {"decimal": 11526027, "binary": 0b101011111101111110001011 },
    "high": {"decimal": 11525963, "binary": 0b101011111101111101001011 },
    "forward": {"decimal": 11526115, "binary": 0b101011111101111111100011 },
    "reverse": {"decimal": 11525667, "binary": 0b101011111101111000100011 },
    "timer_setting_1": {"decimal": None, "binary": None},
    "timer_setting_2": {"decimal": None, "binary": None},
    "timer_setting_3": {"decimal": None, "binary": None},
}

commands_gym = {
    #Gym Room
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


state = {"registered": False}


def registration(device_name):
    """Generate registration message to server"""
    message = {"name": device_name, "capabilities": capabilites}
    return message


device_uuid = "59d84578-e7fb-4c94-ac7f-3769b12a12e1"
API_SERVER = "http://192.168.50.208:8000"

board_led = machine.Pin(16, machine.Pin.OUT)
wifi_led = machine.Pin(2, machine.Pin.OUT)

rfdevice = RFDevice(RADIO_TX_PIN, tx_repeat=1)
rfdevice.enable_tx()

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print("woke from a deep sleep")
else:
    print("power on or hard reset")


def connect_wifi():
    print("Trying to connect to WIFI")

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.scan()
    sta_if.connect("beaches", "472023Beach")
    sta_if.isconnected()
    for x in range(10):
        time.sleep(1)
        if sta_if.isconnected():
            board_led.value(0)
            break
        if x == 9:
            raise Exception("Timedout connecting to wifi")
    return sta_if.ifconfig()


def deep_sleep():
    """This requires RST pin to be connected to D0 (GPIO 16)"""
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, 10000)
    # put the device to sleep
    print("Entering deep sleep")
    # machine.deepsleep()
    time.sleep(10)


def register():
    print(f"Registering device against API server - {API_SERVER}.")
    post_data = registration(device_uuid)
    response = urequests.post(
        f"{API_SERVER}/devices/",
        headers={"Content-Type": "application/json"},
        data=ujson.dumps(post_data),
    )
    status = response.json()["registration"]
    print("Successfully registered:", status)
    if status == "success":
        state["registered"] = True


while True:
    wifi_led.value(0)

    ipaddress, subnetmask, gateway, dns_server = connect_wifi()
    print(f"Device connected: IP: {ipaddress}")

    if not state["registered"]:
        register()

    post_data = ujson.dumps({"device_ip": ipaddress, "time": time.gmtime()})

    print("Checking for new commands")
    response = urequests.get(
        f"{API_SERVER}/devices/{device_uuid}/commands",
        headers={"content-type": "application/json"},
    )
    print(response.json())
    command_name = response.json()["command"]

    if command_name and command_name in commands:
        print(f"Transmitting code - {commands[command_name]["decimal"]}")
        rfdevice.tx_code(commands[command_name]["decimal"])

    wifi_led.value(1)
    deep_sleep()
