import random
import logging
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# logging.basicConfig(level=logging.INFO)

char1 = '012345678901234567890123456789' #30
char2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ∈' #26+1
char3 = 'abcdefghijklmnopqrstuvwxyz' #26
char4 = 'αβγδεζηθικλμνξοπρςστυφχψω' #25
char5 = '-+~.' # 15+5
sup_number = str.maketrans('0123456789', u'\u2070\u00B9\u00B2\u00B3\u2074\u2075\u2076\u2077\u2078\u2079') # 数字上标
sub_number = str.maketrans('0123456789', u'\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089') # 数字下标

# 图片生成位置
filename = "./data/"
# 图片尺寸
pic_size = (120, 50)
# 背景颜色，默认为白色
bg_color = (255, 255, 255)
# 字体颜色，默认为黑
text_color = (0, 0, 0)
# 字体位置
font1 = "./font/times.ttf" # 正常
font2 = "./font/timesi.ttf" #斜体

# 干扰线颜色，默认为红色
line_color = (255, 0, 0)
# 是否加入干扰线
draw_line = True
# 加入干扰线条数上下限
line_number = (1, 5)
# 是否加入干扰点
draw_points = True
# 干扰点出现的概率(%)
point_chance = 1

image = Image.new('RGBA', (pic_size[0], pic_size[1]), bg_color)
font = ImageFont.truetype(font1, 25)
draw = ImageDraw.Draw(image)

def char_len(num):
    """
    # 按比例控制字符长度
    num： 需要生成的图片数量
    return：每张图片对应字符数列表
    """

    numLen = '1234567'
    result = random.choices(numLen, weights=[4,3,6,8,6,2,1], k=num)
    return result

def all_word_type(numlist):
    """
    # 控制不同长度字符时的情况
    numlist： 字符数量列表
    return：
    """

    temp_word = []

    for i in numlist:
        if int(i) == 1:
            """
            只有大写字母
            """
            t1 = random.choice(char2)
            temp_word.append(t1)

        elif int(i) == 2:
            """
            大写开头75%
            罗马开头25%
            """
            char_kind = random.choices('12', weights=[3,1])
            if int(char_kind[0]) == 1:
                r1 = random.choice(char2)
                r2 = random.choice(char1 + char1 + char3 + char4).translate(sub_number) # 若第二个是数字，则全翻译为下标
                temp_word.append(r1 + r2)
            elif int(char_kind[0]) == 2:
                r1 = random.choice(char4)
                r2 = random.choice(char1 + char1 + char3).translate(sub_number)          # 若第二个是数字，则全翻译为下标
                temp_word.append(r1 + r2)

        elif int(i) == 3:
            """
            大写开头70%，
            罗马开头30%，后跟2数字，一上一下
            """
            char_kind = random.choices('12', weights=[7,3])
            if int(char_kind[0]) == 1:
                r1 = random.choice(char2)
                r2 = random.choice(char1 + char2 + char3 + char4 + char5).translate(sup_number)
                r3 = random.choice(char1 + char2 + char3 + char4).translate(sub_number)
                temp_word.append(r1 + r2 + r3)
            elif int(char_kind[0]) == 2:
                r1 = random.choice(char4)
                r2 = random.choice(char1).translate(sup_number) # 上标
                r3 = random.choice(char1).translate(sub_number) # 下标
                temp_word.append(r1 + r2 + r3)

        elif int(i) == 4:
            char_kind = random.choices('12', weights=[9, 1])
            if int(char_kind[0]) == 1:
                r1 = random.choice(char2)
                r2 = random.choice(char1 + char2 + char3 + char4 + char5)
                r3 = random.choice(char1 + char2 + char3 + char4 + char5)
                r4 = random.choice(char1 + char2 + char3 + char4)
                if r2 in char1 and r3 in char1: # 2,3是上下标情况
                    r2 = r2.translate(sup_number)
                    r3 = r3.translate(sub_number)
                    r4 = random.choice(char2 + char3 + char4)
                elif r3 in char1 and r4 in char1: # 3,4是上下标情况
                    r3 = r3.translate(sup_number)
                    r4 = r4.translate(sub_number)
                else:
                    r2 = r2.translate(sub_number)
                    r3 = r3.translate(sub_number)
                    r4 = r4.translate(sub_number)
                temp_word.append(r1 + r2 + r3 + r4)

            elif int(char_kind[0]) == 2:
                r1 = random.choice(char4)
                r2 = random.choice(char1 + char2 + char3 + char4 + char5)
                r3 = random.choice(char1 + char2 + char3 + char4 + char5)
                r4 = random.choice(char1 + char2 + char3 + char4)
                if r2 in char1 and r3 in char1: # 2,3是上下标情况,需要4不是数字
                    r2 = r2.translate(sup_number)
                    r3 = r3.translate(sub_number)
                    r4 = random.choice(char2 + char3 + char4)
                elif r3 in char1 and r4 in char1: # 3,4是上下标情况
                    r3 = r3.translate(sup_number)
                    r4 = r4.translate(sub_number)
                else:
                    r2 = r2.translate(sub_number)
                    r3 = r3.translate(sub_number)
                    r4 = r4.translate(sub_number)
                temp_word.append(r1 + r2 + r3 + r4)

        elif int(i) == 5:
            r1 = random.choice(char2 + char2 + char4) # 首字符为大写字母或罗马，2:1
            r2 = random.choice(char1 + char2 + char3 + char4 + char5)
            r3 = random.choice(char1 + char2 + char3 + char4 + char5)
            r4 = random.choice(char1 + char2 + char3 + char4 + char5)
            r5 = random.choice(char1 + char2 + char3 + char4)
            if r2 in char1 and r3 in char1:  # 2,3是上下标情况,需要4不是数字
                r2 = r2.translate(sup_number)
                r3 = r3.translate(sub_number)
                r4 = random.choice(char2 + char3 + char4 + char5)
                r5 = random.choice(char2 + char3 + char4)
            elif r3 in char1 and r4 in char1:  # 3,4是上下标情况
                r2 = random.choice(char2 + char3 + char4 + char5)
                r3 = r3.translate(sup_number)
                r4 = r4.translate(sub_number)
                r5 = random.choice(char2 + char3 + char4)
            elif r4 in char1 and r5 in char1: # 4,5 是上下标情况
                r4 = r4.translate(sup_number)
                r5 = r5.translate(sub_number)
                r2 = random.choice(char2 + char3 + char4 + char5)
                r3 = random.choice(char2 + char3 + char4 + char5)
            else:
                r2 = r2.translate(sub_number)
                r3 = r3.translate(sub_number)
                r4 = r4.translate(sub_number)
                r5 = r5.translate(sub_number)
            temp_word.append(r1 + r2 + r3 + r4 + r5)

        elif int(i) == 6:
            r1 = random.choice(char2 + char4)
            r2 = random.choice(char1 + char2 + char3 + char4 + char5)
            r3 = random.choice(char1 + char2 + char3 + char4 + char5)
            r4 = random.choice(char1 + char2 + char3 + char4 + char5)
            r5 = random.choice(char1 + char2 + char3 + char4 + char5)
            r6 = random.choice(char1 + char2 + char3 + char4)
            if r2 in char1 and r3 in char1:  # 2,3是上下标情况,需要4不是数字
                r2 = r2.translate(sup_number)
                r3 = r3.translate(sub_number)
                r4 = random.choice(char2 + char3 + char4 + char5)
                r5 = random.choice(char2 + char3 + char4 + char5)
                r6 = random.choice(char2 + char3 + char4)
            elif r3 in char1 and r4 in char1:  # 3,4是上下标情况
                r3 = r3.translate(sup_number)
                r4 = r4.translate(sub_number)
                r2 = random.choice(char2 + char3 + char4 + char5)
                r5 = random.choice(char2 + char3 + char4 + char5)
                r6 = random.choice(char2 + char3 + char4 )

            elif r4 in char1 and r5 in char1: # 4,5 是上下标情况
                r4 = r4.translate(sup_number)
                r5 = r5.translate(sub_number)
                r2 = random.choice(char2 + char3 + char4 + char5)
                r3 = random.choice(char2 + char3 + char4 + char5)
                r6 = random.choice(char2 + char3 + char4)
            elif r5 in char1 and r6 in char1: # 5,6是上下标情况
                r5 = r5.translate(sup_number)
                r6 = r6.translate(sub_number)
                r2 = random.choice(char2 + char3 + char4 + char5)
                r3 = random.choice(char2 + char3 + char4 + char5)
                r4 = random.choice(char2 + char3 + char4 + char5)
            else:
                r2 = r2.translate(sub_number)
                r3 = r3.translate(sub_number)
                r4 = r4.translate(sub_number)
                r5 = r5.translate(sub_number)
                r6 = r6.translate(sub_number)

            temp_word.append(r1 + r2 + r3 + r4 + r5 + r6)

        elif int(i) == 7:
            r1 = random.choice(char2 + char2 + char4)
            r2 = random.choice(char1 + char2 + char3 + char4 + char5).translate(sub_number)
            r3 = random.choice(char1 + char2 + char3 + char4 + char5).translate(sub_number)
            r4 = random.choice(char1 + char2 + char3 + char4 + char5).translate(sub_number)
            r5 = random.choice(char1 + char2 + char3 + char4 + char5).translate(sub_number)
            r6 = random.choice(char1 + char2 + char3 + char4 + char5).translate(sub_number)
            r7 = random.choice(char1 + char2 + char3 + char4)
            temp_word.append(r1 + r2 + r3 + r4 + r5 + r6 + r7)

    return temp_word

# print(all_word_type(char_len(30)))

# 随机选择字体
def choose_font():
    char_kind = random.choices('12', weights=[9, 1])
    if int(char_kind[0]) == 1:
        font = font1
    else:
        font = font2
    return font

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

# 随机生成干扰线
def gene_line(draw, pic_size):
    line_color = choose_bgColor()
    begin = (random.randint(0, pic_size[0]), random.randint(0, pic_size[1]))
    end = (random.randint(0, pic_size[0]), random.randint(0, pic_size[1]))
    draw.line([begin, end], fill=line_color)

# 随机绘制干扰点
def gene_points(draw, pic_size, point_chance):
    for w in range(pic_size[0]):
        for h in range(pic_size[1]):
            tmp = random.randint(0, 100)
            if tmp > 100 - point_chance:
                draw.point((w, h), fill=(0, 0, 0))

# 随机生成图片，num为张数
def gene_GeoPic(num = 1, pic_size = (120, 50)):

    text_list = all_word_type(char_len(num))
    for text in text_list:
        bg_color = choose_bgColor()
        width, height = pic_size  # 宽和高
        image = Image.new('RGBA', (width, height), bg_color)  # 创建图片
        font = ImageFont.truetype(font1, 20)
        draw = ImageDraw.Draw(image)  # 创建画笔

        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / len(text),
                   (height - font_height) / len(text)),
                  text,
                  font= font,
                  fill=text_color)

        if draw_line:
            n = random.randint(line_number[0], line_number[1])
            for i in range(n):
                gene_line(draw, pic_size)
        if draw_points:
            gene_points(draw, pic_size, point_chance)

        # params = [1 - float(random.randint(1, 2)) / 100,
        #           0,
        #           0,
        #           0,
        #           1 - float(random.randint(1, 10)) / 100,
        #           float(random.randint(1, 2)) / 500,
        #           0.001,
        #           float(random.randint(1, 2)) / 500
        #           ]
        # image = image.transform((pic_size[0], pic_size[1]), Image.PERSPECTIVE, params)  # 创建扭曲
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 边界加强

        aa = str(".png")
        path = filename + text + aa
        image.save(path)


gene_GeoPic(100)



