import time
import panel
import font
from neopixel_panel import NeopixelPanel
import colors
import network
import secrets

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

# t = time.localtime()
# panel.display_string_at(0, 1, f'{t[3]}:{t[4]}', font, color)

# black = (0,0,0)
# time.sleep(2)
# panel.clear()
# panel.draw_horizontal_line(0, 2, 32, color)
# 
# 
# panel.draw_vertical_line(20, 0, 8, color)

for i in range(11):
    panel.clear()
    panel.display_string_at(0, 1, f'{i}', font, color)
    panel.show()
# 
# 
# panel.draw_rectangle(2, 2, 4,4, color)
# 
# 
# panel.draw_filled_rectangle(0, 0, 16,4, color)
# 
# 
# panel.draw_circle(18, 4, 3, color)
time.sleep(10)
panel.clear()