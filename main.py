import time
import picoNeopixelMatrix.default_font as font
from picoNeopixelMatrix.neopixel_panel import NeopixelPanel
import colors
import network
import secrets
import ntptime
import machine

color = colors.AQUAMARINE4
panel = NeopixelPanel(32, 8, 0, 0, "GRB")
panel.brightness(80)

def diplay_print(mes, mes_color = color):
    print(mes)
    if "ETIMEDOUT" in str(mes):
        mes = "time"
    elif "OSError" in str(mes):
        mes = "os"
    panel.clear()
    panel.display_string_at(0, 1, f'{mes}', font, mes_color)
    panel.show()
    
def cettime():
    year = time.localtime()[0]       #get current year
    HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to CEST
    HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
    now=time.time()
    if now < HHMarch :               # we are before last sunday of march
        cet=time.localtime(now+3600) # CET:  UTC+1H
    elif now < HHOctober :           # we are before last sunday of october
        cet=time.localtime(now+7200) # CEST: UTC+2H
    else:                            # we are after last sunday of october
        cet=time.localtime(now+3600) # CET:  UTC+1H
    return(cet)

def settime():
    error = True
    ntptime.timeout = 2
    while error:
        try:
            ntptime.settime()
            error = False
        except Exception as e:
            time.sleep(1)
            print(e)
            print("Error setting time")
            pass
        
def show_time(hour, minutes, color = color):
    if len(str(minutes)) < 2:
        minutes = f'0{minutes}'
    if len(str(hour)) < 2:
        hour = f'0{hour}'
    panel.clear()
    panel.display_string_at(0, 1, f'{hour}:{minutes}', font, color)
    panel.show()

def connect_wifi():
    network.hostname("mini_me")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.disconnect()
    sta_if.connect(secrets.SSID, secrets.PASSWORD)
    while not sta_if.isconnected():
        print("connectig....")
        panel.show()
        time.sleep(0.3)
    diplay_print("WI FI OK")
    print("connected")
        
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
    for i in range(128):    
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

# Cleanup before the start
# fix for https://github.com/blaz-r/pi_pico_neopixel/issues/9
rp2.PIO(0).remove_program()
panel.clear()
panel.show()

connect_wifi()

settime()
t = cettime()
show_time(t[3], t[4], color)

print("start time loop")
while True:
    t2 = cettime()
    if t[3] < t2[3] or t[4] < t2[4]:
        t = t2
        if t[3] == 19 and t[4] == 0:
            print("chasing rainbow")
            chasing_rainbow()
        show_time(t[3], t[4], color)
        seconds = 59 - cettime()[5]
        time.sleep(seconds)

