#coding:utf-8

import cv2
import numpy as np
import random
import sys
from crnn import CRNN
from PIL import Image,ImageFont,ImageDraw
import tensorflow as tf
import utils
from tensorflow.contrib import rnn
# import ocr.crnn_tf.config as config

# 元数据集
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# DIGITS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
#           'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
#           'α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','ς','σ','τ','υ','φ','χ','ψ','ω',
#           '₀','₁','₂','₃','₄','₅','₆','₇','₈','₉','-']

data_dir = './data/'
model_dir = './model/'

class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
	    self.terminal = stream
	    self.log = open(filename, 'a', encoding='utf-8')

    def write(self, message):
	    self.terminal.write(message)
	    self.log.write(message)

    def flush(self):
	    pass

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
    # 设置字体、大小
    text_color = (0, 0, 0)     # 字体颜色，默认为黑
    font_path = "./font/times.ttf"
    font_size = 30
    font=ImageFont.truetype(font_path,font_size)

    for i in range(cnt):
        # 随机背景颜色
        bg_color = choose_bgColor()

        # 随机生成1到7位的不定长数字
        rnd = random.randint(1, 7)
        text = ''
        for j in range(rnd):
            text = text + DIGITS[random.randint(0, len(DIGITS) - 1)]

        # 生成图片并绘上文字
        img=Image.new("RGB", (256,32), bg_color)
        draw=ImageDraw.Draw(img)
        draw.text((1,1),text,font=font,fill=text_color)
        img=np.array(img)

        # 随机叠加椒盐噪声并保存图像
        img = img_salt_pepper_noise(img, float(random.randint(1,3)/100.0))
        # cv2.imwrite(data_dir + text + '_' + str(i+1) + '.jpg',img)
        output_path = data_dir + text + '_' + str(i + 1) + '.jpg'
        cv2.imencode('.jpg', img)[1].tofile(output_path)



# 模型训练
def train():

    batch_size=32
    max_image_width=400
    train_test_ratio=0.75
    restore=True
    iteration_count=1000

    crnn = CRNN(
        batch_size,
        model_dir,
        data_dir,
        max_image_width,
        train_test_ratio,
        restore
    )

    crnn.train(iteration_count)

# 模型测试
def test():

    # 设置基本属性
    batch_size=32
    max_image_width=400
    restore=True

    # 初始化CRNN
    crnn = CRNN(
        batch_size,
        model_dir,
        data_dir,
        max_image_width,
        0,
        restore
    )

    # 测试模型
    crnn.test()

# # CRNN 网络结构
# def crnn_network(max_width, batch_size):
#     # 双向RNN
#     def BidirectionnalRNN(inputs, seq_len):
#         # rnn-1
#         with tf.variable_scope(None, default_name="bidirectional-rnn-1"):
#             # Forward
#             lstm_fw_cell_1 = rnn.BasicLSTMCell(256)
#             # Backward
#             lstm_bw_cell_1 = rnn.BasicLSTMCell(256)
#             inter_output, _ = tf.nn.bidirectional_dynamic_rnn(lstm_fw_cell_1, lstm_bw_cell_1, inputs, seq_len, dtype=tf.float32)
#             inter_output = tf.concat(inter_output, 2)
#
#         # rnn-2
#         with tf.variable_scope(None, default_name="bidirectional-rnn-2"):
#             # Forward
#             lstm_fw_cell_2 = rnn.BasicLSTMCell(256)
#             # Backward
#             lstm_bw_cell_2 = rnn.BasicLSTMCell(256)
#             outputs, _ = tf.nn.bidirectional_dynamic_rnn(lstm_fw_cell_2, lstm_bw_cell_2, inter_output, seq_len, dtype=tf.float32)
#             outputs = tf.concat(outputs, 2)
#         return outputs
#
#     # CNN，用于提取特征
#     def CNN(inputs):
#         # 64 / 3 x 3 / 1 / 1
#         conv1 = tf.layers.conv2d(inputs=inputs, filters = 64, kernel_size = (3, 3), padding = "same", activation=tf.nn.relu)
#         # 2 x 2 / 1
#         pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)
#         # 128 / 3 x 3 / 1 / 1
#         conv2 = tf.layers.conv2d(inputs=pool1, filters = 128, kernel_size = (3, 3), padding = "same", activation=tf.nn.relu)
#         # 2 x 2 / 1
#         pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)
#         # 256 / 3 x 3 / 1 / 1
#         conv3 = tf.layers.conv2d(inputs=pool2, filters = 256, kernel_size = (3, 3), padding = "same", activation=tf.nn.relu)
#         # Batch normalization layer
#         bnorm1 = tf.layers.batch_normalization(conv3)
#         # 256 / 3 x 3 / 1 / 1
#         conv4 = tf.layers.conv2d(inputs=bnorm1, filters = 256, kernel_size = (3, 3), padding = "same", activation=tf.nn.relu)
#         # 1 x 2 / 1
#         pool3 = tf.layers.max_pooling2d(inputs=conv4, pool_size=[2, 2], strides=[1, 2], padding="same")
#         # 512 / 3 x 3 / 1 / 1
#         conv5 = tf.layers.conv2d(inputs=pool3, filters = 512, kernel_size = (3, 3), padding = "same", activation=tf.nn.relu)
#         # Batch normalization layer
#         bnorm2 = tf.layers.batch_normalization(conv5)
#         # 512 / 3 x 3 / 1 / 1
#         conv6 = tf.layers.conv2d(inputs=bnorm2, filters = 512, kernel_size = (3, 3), padding = "same", activation=tf.nn.relu)
#         # 1 x 2 / 2
#         pool4 = tf.layers.max_pooling2d(inputs=conv6, pool_size=[2, 2], strides=[1, 2], padding="same")
#         # 512 / 2 x 2 / 1 / 0
#         conv7 = tf.layers.conv2d(inputs=pool4, filters = 512, kernel_size = (2, 2), padding = "valid", activation=tf.nn.relu)
#         return conv7
#
#     # 定义输入、输出、序列长度
#     inputs = tf.placeholder(tf.float32, [batch_size, max_width, 32, 1])
#     targets = tf.sparse_placeholder(tf.int32, name='targets')
#     seq_len = tf.placeholder(tf.int32, [None], name='seq_len')
#
#     # 卷积层提取特征
#     cnn_output = CNN(inputs)
#     reshaped_cnn_output = tf.reshape(cnn_output, [batch_size, -1, 512])
#     max_char_count = reshaped_cnn_output.get_shape().as_list()[1]
#
#     # 循环层处理序列
#     crnn_model = BidirectionnalRNN(reshaped_cnn_output, seq_len)
#     logits = tf.reshape(crnn_model, [-1, 512])
#
#     # 转录层预测结果
#     W = tf.Variable(tf.truncated_normal([512, config.NUM_CLASSES], stddev=0.1), name="W")
#     b = tf.Variable(tf.constant(0., shape=[config.NUM_CLASSES]), name="b")
#     logits = tf.matmul(logits, W) + b
#     logits = tf.reshape(logits, [batch_size, -1, config.NUM_CLASSES])
#     logits = tf.transpose(logits, (1, 0, 2))
#
#     # 定义损失函数、优化器
#     loss = tf.nn.ctc_loss(targets, logits, seq_len)
#     cost = tf.reduce_mean(loss)
#     optimizer = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost)
#     decoded, log_prob = tf.nn.ctc_beam_search_decoder(logits, seq_len, merge_repeated=False)
#     dense_decoded = tf.sparse_tensor_to_dense(decoded[0], default_value=-1)
#     acc = tf.reduce_mean(tf.edit_distance(tf.cast(decoded[0], tf.int32), targets))
#
#     # 初始化
#     init = tf.global_variables_initializer()
#
#     return inputs, targets, seq_len, logits, dense_decoded, optimizer, acc, cost, max_char_count, init
#
# # CRNN 识别文字
# # 输入：图片路径
# # 输出：识别文字结果
# def predict(img_path):
#
#     # 定义模型路径、最长图片宽度
#     batch_size = 1
#     model_path = '/tmp/crnn_model/'
#     max_image_width = 400
#
#     # 创建会话
#     __session = tf.Session()
#     with __session.as_default():
#         (
#             __inputs,
#             __targets,
#             __seq_len,
#             __logits,
#             __decoded,
#             __optimizer,
#             __acc,
#             __cost,
#             __max_char_count,
#             __init
#         ) = crnn_network(max_image_width, batch_size)
#         __init.run()
#
#     # 加载模型
#     with __session.as_default():
#         __saver = tf.train.Saver()
#         ckpt = tf.train.latest_checkpoint(model_path)
#         if ckpt:
#             __saver.restore(__session, ckpt)
#
#     # 读取图片作为输入
#     arr, initial_len = utils.resize_image(img_path,max_image_width)
#     batch_x = np.reshape(
#         np.array(arr),
#         (-1, max_image_width, 32, 1)
#     )
#
#     # 利用模型识别文字
#     with __session.as_default():
#         decoded = __session.run(
#             __decoded,
#             feed_dict={
#                 __inputs: batch_x,
#                 __seq_len: [__max_char_count] * batch_size
#             }
#         )
#         pred_result = utils.ground_truth_to_word(decoded[0])
#
#     return pred_result


if __name__ == '__main__':
    train()