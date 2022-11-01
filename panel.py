import utime
from neopixel import Neopixel


class Panel:
    
    def __init__(self, width, height):
        self.pixels = Neopixel( width * height, 0, 28, "GRB")
        self.width = width # x
        self.height = height # y
        
    def init(self):
        return 0

    def clear(self):
        black = (0,0,0)
        self.pixels.fill(black)
        self.pixels.show()

    def show(self):
        self.pixels.show()
        
    def set_pixel(self, x, y, color):
        if (x < 0 or x >= self.width or y < 0 or y >= self.height):
            return
        self.set_absolute_pixel(x, y, color)

    def set_absolute_pixel(self, x, y, color):
        if (x % 2) == 1:
            index = 255 - (x * self.height + y)
        else:
            index = 255 - ((x+1) * self.height - (y+1))

        self.pixels.set_pixel(index, color)
            
    def draw_char_at(self, x, y, char, font, color):
        char_offset = (ord(char) - ord(' ')) * font.height * (int(font.width / 8) + (1 if font.width % 8 else 0))
        
        offset = 0
        width = 1
        for w in font.data[char_offset+offset:char_offset+offset+font.height]:
            try:
                binary = "{0:b}".format(w).encode('UTF-8')
                i = binary.rindex(b'1') + 2
                if i > width:
                    width = i
            except Exception as e:
                pass
        
        for j in range(font.height):
            for i in range(width):
                if font.data[char_offset+offset] & (0x80 >> (i % 8)):
                    self.set_pixel(x + i, y + j, color)
                if i % 8 == 7:
                    offset += 1
            if width % 8 != 0:
                offset += 1                
        return width

    def display_string_at(self, x, y, text, font, color):
        refcolumn = x

        # Send the string character by character on PANEL
        for index in range(len(text)):
            # Display one character on PANEL
            width = self.draw_char_at(refcolumn, y, text[index], font, color)
            # Decrement the column position by 16
            refcolumn += width


    def draw_line(self, x0, y0, x1, y1, color):
        # Bresenham algorithm
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while((x0 != x1) and (y0 != y1)):
            self.set_pixel(x0, y0 , color)
            if (2 * err >= dy):
                err += dy
                x0 += sx
            if (2 * err <= dx):
                err += dx
                y0 += sy

    def draw_horizontal_line(self, x, y, width, color):
        for i in range(x, x + width):
            self.set_pixel(i, y, color)

    def draw_vertical_line(self, x, y, height, color):
        for i in range(y, y + height):
            self.set_pixel(x, i, color)

    def draw_rectangle(self, x0, y0, x1, y1, color):
        min_x = x0 if x1 > x0 else x1
        max_x = x1 if x1 > x0 else x0
        min_y = y0 if y1 > y0 else y1
        max_y = y1 if y1 > y0 else y0
        self.draw_horizontal_line(min_x, min_y, max_x - min_x + 1, color)
        self.draw_horizontal_line(min_x, max_y, max_x - min_x + 1, color)
        self.draw_vertical_line(min_x, min_y, max_y - min_y + 1, color)
        self.draw_vertical_line(max_x, min_y, max_y - min_y + 1, color)

    def draw_filled_rectangle(self, x0, y0, x1, y1, color):
        min_x = x0 if x1 > x0 else x1
        max_x = x1 if x1 > x0 else x0
        min_y = y0 if y1 > y0 else y1
        max_y = y1 if y1 > y0 else y0
        for i in range(min_x, max_x + 1):
            self.draw_vertical_line(i, min_y, max_y - min_y + 1, color)

    def draw_circle(self, x, y, radius, color):
        # Bresenham algorithm
        x_pos = -radius
        y_pos = 0
        err = 2 - 2 * radius
        if (x >= self.width or y >= self.height):
            return
        while True:
            self.set_pixel(x - x_pos, y + y_pos, color)
            self.set_pixel(x + x_pos, y + y_pos, color)
            self.set_pixel(x + x_pos, y - y_pos, color)
            self.set_pixel(x - x_pos, y - y_pos, color)
            e2 = err
            if (e2 <= y_pos):
                y_pos += 1
                err += y_pos * 2 + 1
                if(-x_pos == y_pos and e2 <= x_pos):
                    e2 = 0
            if (e2 > x_pos):
                x_pos += 1
                err += x_pos * 2 + 1
            if x_pos > 0:
                break

    def draw_filled_circle(self, x, y, radius, color):
        # Bresenham algorithm
        x_pos = -radius
        y_pos = 0
        err = 2 - 2 * radius
        if (x >= self.width or y >= self.height):
            return
        while True:
            self.set_pixel(x - x_pos, y + y_pos, color)
            self.set_pixel(x + x_pos, y + y_pos, color)
            self.set_pixel(x + x_pos, y - y_pos, color)
            self.set_pixel(x - x_pos, y - y_pos, color)
            self.draw_horizontal_line(x + x_pos, y + y_pos, 2 * (-x_pos) + 1, color)
            self.draw_horizontal_line(x + x_pos, y - y_pos, 2 * (-x_pos) + 1, color)
            e2 = err
            if (e2 <= y_pos):
                y_pos += 1
                err += y_pos * 2 + 1
                if(-x_pos == y_pos and e2 <= x_pos):
                    e2 = 0
            if (e2 > x_pos):
                x_pos  += 1
                err += x_pos * 2 + 1
            if x_pos > 0:
                break
