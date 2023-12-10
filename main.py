import time
import picoNeopixelMatrix.default_font as font
from picoNeopixelMatrix.neopixel_panel import NeopixelPanel
import colors
import network
import secrets
from weather import Weather
import struct
import socket

NTP_DELTA = 2208988800
host = "pool.ntp.org"
port = 123
color = colors.AQUAMARINE4

panel = NeopixelPanel(32, 8, 0, 0, "GRB")
panel.brightness(80)

def diplay_print(mes, error_color = color):
    print(mes)
    if "ETIMEDOUT" in str(mes):
        mes = "time"
    elif "OSError" in str(mes):
        mes = "os"
    panel.clear()
    panel.display_string_at(0, 1, f'{mes}', font, error_color)
    panel.show()

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    print("hi")
    while True:
        try:        
            msg = s.recv(48)
            print("hi2")
        except OSError as e:
            diplay_print(e)
            time.sleep(5)
            continue
        break
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

def show_time(hour, minutes, color = color):
    if len(str(minutes)) < 2:
        minutes = f'0{minutes}'
    if len(str(hour)) < 2:
        hour = f'0{hour}'
    panel.clear()
    panel.display_string_at(0, 1, f'{hour}:{minutes}', font, color)
    panel.show()

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.active(False)
    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    while not wlan.isconnected():
        print("connectig....")
        panel.display_string_at(0, 1, "3", font, color)
        panel.show()
        time.sleep(0.3)
    print("connected")
    diplay_print(wlan.ifconfig()[0])

def party_panel():
    for i in range(30):
        panel.clear()
        panel.fill(colors.MINT)
        panel.show()
        
def chasing_rainbow():
    x_positions = {
        "redx": 0, "redx1": 5,
        "yelx": 5, "yelx1": 10,
        "grex": 10, "grex1": 15,
        "cyax": 15, "cyax1": 20,
        "blux": 20, "blux1": 25,
        "purx": 25, "purx1": 32
    }
    rainbow_colors = [colors.RED1, colors.YELLOW1,colors.GREEN1,colors.CYAN2,colors.BLUE,colors.PURPLE1]
    for i in range(6400):    
        panel.draw_filled_rectangle(x_positions["redx"],0,x_positions["redx1"],8, colors.RED1)
        panel.draw_filled_rectangle(x_positions["yelx"],0,x_positions["yelx1"],8, colors.YELLOW1)
        panel.draw_filled_rectangle(x_positions["grex"],0,x_positions["grex1"],8, colors.GREEN1)
        panel.draw_filled_rectangle(x_positions["cyax"],0,x_positions["cyax1"],8, colors.CYAN2)
        panel.draw_filled_rectangle(x_positions["blux"],0,x_positions["blux1"],8, colors.BLUE)
        panel.draw_filled_rectangle(x_positions["purx"],0,x_positions["purx1"],8, colors.PURPLE1)
        panel.show()
        for pos, num in x_positions.items():
            if num == 32:
                x_positions[pos] = 0
            else:
                x_positions[pos] = x_positions[pos] + 1
#     colors for rainbow
#     color_chase(RED, 0.1)  5
#     color_chase(YELLOW, 0.1) 5
#     color_chase(GREEN, 0.1) 5
#     color_chase(CYAN, 0.1) 5
#     color_chase(BLUE, 0.1) 5
#     color_chase(PURPLE, 0.1) 6 Rows

# fix for https://github.com/blaz-r/pi_pico_neopixel/issues/9
rp2.PIO(0).remove_program()

# Enable once I have a proper wifi router.
# connect_wifi()
# set_time()

t = time.localtime()

chasing_rainbow()

show_time(t[3], t[4], color)

while True:
    t2 = time.localtime()
    if t[3] < t2[3] or t[4] < t2[4]:
        t = t2
        if t[3] == "19" or t[4] == "0":
            party_panel()
        show_time(t[3], t[4], color)
        time.sleep(58)