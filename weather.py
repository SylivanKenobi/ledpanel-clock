import urequests

class Weather:

    def __init__(self):
        pass
    
    def get_temp(self):
        r = requests.get("https://www.bbc.com/weather/2661552")
        con = str(r.content)
        start = con.find("wr-value--temperature--c") + len("wr-value--temperature--c")
        end = con.find("\\xc2\\xb0")
        print(con[start + 2:end])
        return con[start + 2:end]
