import opc
from time import sleep

from colour import Color

LEDS = 30


def set_neopixel_color(rbg_tuple):
    client = opc.Client('localhost:7890')
    print(rbg_tuple)
    pixels = [rbg_tuple] * LEDS
    client.put_pixels(pixels)
    client.put_pixels(pixels)


def generate_color_range(num_colors, color1, color2):
    print(color1, color2, num_colors)
    col1 = Color(color1)
    col2 = Color(color2)
    return col2.range_to(col1, num_colors)


def fade_neopixel(color1, color2, num_colors, delay):
    client = opc.Client('localhost:7890')
    color_range = generate_color_range(num_colors, color1, color2)
    for color in color_range:
        rgb = (color.get_red(), color.get_green(), color.get_blue())
        rgb = tuple(i * 220 for i in rgb)
        print(rgb)
        pixels = [rgb] * LEDS
        client.put_pixels(pixels)
        client.put_pixels(pixels)
        sleep(delay)


def create_color(color):
    color = Color(color.title())
    rgb = (color.get_red(), color.get_green(), color.get_blue())
    return tuple(i * 255 for i in rgb)
