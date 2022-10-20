import time
import panel
import font
from neopixel import Neopixel
import colors
import network
import secrets

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
wlan.connect(secrets.SSID, secrets.PASSWORD)

while not wlan.isconnected():
    print("connectig....")
    time.sleep(0.5)
print("connected")
t = time.localtime()

color = colors.AQUA
# fix for https://github.com/blaz-r/pi_pico_neopixel/issues/9
rp2.PIO(0).remove_program()

panel = panel.Panel(32, 8)
panel.init()

ppanel.display_string_at(2, 2, f'{t[3]}:{t[4]}:{t[5]}', font, color)
black = (0,0,0)
time.sleep(2)
panel.clear()
panel.draw_horizontal_line(0, 2, 32, color)
time.sleep(2)
panel.clear()

panel.draw_vertical_line(2, 2, 4, color)
time.sleep(2)
panel.clear()

panel.draw_rectangle(2, 2, 4,4, color)


panel.draw_filled_rectangle(8, 2, 10,12, color)
time.sleep(2)
panel.clear()

panel.draw_circle(2, 2, 2, color)
time.sleep(2)
panel.clear()
