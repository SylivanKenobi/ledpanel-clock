import time
import panel
import font
from neopixel import Neopixel
import colors

color = colors.AQUA
# fix for https://github.com/blaz-r/pi_pico_neopixel/issues/9
rp2.PIO(0).remove_program()

panel = panel.Panel(32, 8)
panel.init()

panel.display_string_at(2, 2, "12:35asdasd", font, color)

time.sleep(5)

numpix = 257
pixels = Neopixel(numpix, 0, 28, "GRB")

black = (0,0,0)
pixels.fill(black)

#     
pixels.show()


