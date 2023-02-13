import time
import picoNeopixelMatrix.default_font as font
from picoNeopixelMatrix.neopixel_panel import NeopixelPanel
import colors
import network
import secrets
from weather import Weather

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
wlan.connect(secrets.SSID, secrets.PASSWORD)

while not wlan.isconnected():
    print("connectig....")
    time.sleep(0.3)
print("connected")
# 
color = colors.AQUAMARINE4 
# fix for https://github.com/blaz-r/pi_pico_neopixel/issues/9
rp2.PIO(0).remove_program()

panel = NeopixelPanel(32, 8, 0, 28, "GRB")

t = time.localtime()
panel.display_string_at(0, 1, f'{t[3]}:{t[4]}', font, color)

panel.show()