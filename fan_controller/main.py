import network
import urequests
import ujson
import machine
import time
import commands
import mip

device_uuid = "59d84578-e7fb-4c94-ac7f-3769b12a12e1"

board_led = machine.Pin(16,  machine.Pin.OUT)
wifi_led =  machine.Pin(2,  machine.Pin.OUT)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')


def connect_wifi():

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
    ''' This requires RST pin to be connected to D0 (GPIO 16) '''
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, 10000)
    # put the device to sleep
    print('Entering deep sleep')
    #machine.deepsleep()
    time.sleep(10)


def register():
    post_data = commands.registration(device_uuid)
    print(post_data)
    response = urequests.post(
        "http://10.194.1.111/fans/register/",
        headers = {'content-type': 'application/json'},
        data = ujson.dumps(post_data)
    )
    print(response.json())
    device_id = response.json()['device_id']
    print('Successfully registered:', device_id)

while True:
    wifi_led.value(0)

    ipaddress, subnetmask, gateway, dns_server = connect_wifi()
    print(ipaddress, subnetmask, gateway, dns_server)

    register()

    post_data = ujson.dumps({ "device_ip": ipaddress, "time": time.gmtime()})
    
    print('Sent Data')
    response = urequests.post(
        "http://10.194.1.111/fans/poll/",
        headers = {'content-type': 'application/json'},
        data = post_data
    )
    wifi_led.value(1)
    deep_sleep()