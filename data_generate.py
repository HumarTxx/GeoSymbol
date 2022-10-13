#coding:utf-8

import numpy as np
import cv2
import random
from PIL import Image,ImageFont,ImageDraw

DIGITS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
          'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          'α','β','γ','δ','ε','ζ','η','θ','λ','μ','ν','ξ','π','ρ','ς','σ','τ','υ','φ','χ','ψ','ω',
          '₀','₁','₂','₃','₄','₅','₆','₇','₈','₉',
          '-','+','~','.']

# 上标
sup_number = str.maketrans('0123456789', u'\u2070\u00B9\u00B2\u00B3\u2074\u2075\u2076\u2077\u2078\u2079')
# 下标
sub_number = str.maketrans('0123456789', u'\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089')
origin_number = str.maketrans(u'\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089', '0123456789')

data_dir = './data_tmp/'

# 随机生成干扰线
def gene_line(draw, pic_size):
    line_color = choose_bgColor()
    begin = (random.randint(0, pic_size[0]), random.randint(0, pic_size[1]))
    end = (random.randint(0, pic_size[0]), random.randint(0, pic_size[1]))
    draw.line([begin, end], fill=line_color)

#椒盐噪声
def img_salt_pepper_noise(src,percetage):
    NoiseImg=src
    NoiseNum=int(percetage*src.shape[0]*src.shape[1])
    for i in range(NoiseNum):
        randX=random.randint(0,src.shape[0]-1)
        randY=random.randint(0,src.shape[1]-1)
        if random.randint(0,1)==0:
            NoiseImg[randX,randY]=0
        else:
            NoiseImg[randX,randY]=255
    return NoiseImg
# 随机选择颜色
def choose_bgColor():
    R = random.randint(0, 255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)
    if R == 0 and G == 0 and B == 0:
        R = 255
        G = 255
        B = 255
    return (R, G, B)
# 随机生成不定长数据
def gen_text(cnt):
    # text = text.translate(sup_number)
    # print(text)
    # 设置字体、大小
    text_color = (0, 0, 0)     # 字体颜色，默认为黑
    font_path = "./GeoTest/font/times.ttf"
    font_size = 30
    font=ImageFont.truetype(font_path,font_size)

    file = open('./data_tmp/image_list.txt', 'w', encoding='utf-8')

    for i in range(cnt):
        # 随机背景颜色
        bg_color = choose_bgColor()

        # 随机生成1到7位的不定长数字
        rnd = random.randint(1, 7)

        text = ''
        for j in range(rnd):
            text = text + DIGITS[random.randint(0, len(DIGITS) - 1)]
        # text = 'Ar₃ -Pt₁'

        # 生成图片并绘上文字
        img=Image.new("RGB", (100,32), bg_color)
        draw=ImageDraw.Draw(img)
        draw.text((1,1),text,font=font,fill=text_color)

        gene_line(draw, (100,30))
        gene_line(draw, (100,30))
        gene_line(draw, (100,30))


        img=np.array(img)

        # 随机叠加椒盐噪声并保存图像
        img = img_salt_pepper_noise(img, float(random.randint(1,3)/100.0))
        # cv2.imwrite(data_dir + text + '_' + str(i+1) + '.jpg',img)
        output_path = data_dir + str(i + 1) + '_' + text + '.jpg'
        cv2.imencode('.jpg', img)[1].tofile(output_path)

        file.write(str(i + 1) + '_' + text.translate(origin_number) + '.jpg' + ' ' + text.translate(origin_number) + '\n')
    file.close()

if __name__ == '__main__':
    gen_text(100)
