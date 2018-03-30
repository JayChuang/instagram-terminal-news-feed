# Modified from https://github.com/nilesr/braille-art

from PIL import Image, ImageFilter
from color.img2txt import draw_with_color
import os, random, sys
import subprocess
import time

def img_average(x1, y1, x2, y2, img):
    average = lambda x: sum(x)/len(x) if len(x) > 0 else 0
    ret = []
    for x in range(x1, x2):
        for y in range(y1, y2):
            ret.append(img.getpixel((x, y))[0])
    return average(ret)

def convert_index(x):
    if x == 0: return 1
    if x == 1: return 2
    if x == 2: return 4
    if x == 3: return 64
    if x == 4: return 8
    if x == 5: return 16
    if x == 6: return 32
    if x == 7: return 128

def draw(img_path, post_info):
    img = Image.open(img_path).convert('LA').resize((128, 128), Image.BILINEAR).filter(ImageFilter.CONTOUR)
    start = 0x2800
    char_width = 2
    char_height = char_width * 2
    dither, sensitivity = 5, 0.9*0xFF
    char_width_divided, char_height_divided = round(char_width / 2), round(char_height / 4)
    print('username: ' + post_info['username'])
    print('\033[4m' + post_info['site_url'] + '\033[0m \n')
    out = ""
    for y in range(0, img.height - char_height - 1, char_height):
        for x in range(0, img.width - char_width - 1, char_width):
            byte, index = 0x0, 0
            for xn in range(2):
                for yn in range(4):
                    avg = img_average(x + (char_height_divided * xn), y + (char_width_divided * yn), x + (char_height_divided * (xn + 1)), y + (char_width_divided * (yn + 1)), img)
                    if (avg) > (sensitivity):
                        byte += convert_index(index)
                    index += 1
            out += chr(start + byte)
        out += '\n'
    print(out)
    print('Likes: ' + post_info['likes'])
    print(post_info['caption'])
    print('-------------------\n')

def display_to_terminal(posts_info, display_color):
    file_list = os.listdir('./images/')
    for filename in file_list:
        img_path = './images/' + filename
        if display_color:
            draw_with_color(img_path, posts_info[filename])
            time.sleep(2)
        else:
            draw(img_path, posts_info[filename])

if __name__ == '__main__':
    display_to_terminal(posts_info)
