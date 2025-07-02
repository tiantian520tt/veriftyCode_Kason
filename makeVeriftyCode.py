import random
import numpy as np
from PIL import Image
import imageio
import os
import shutil
import time

lettersCover = []
fps = 90 # 帧率
width = 500 #长
height = 100 #宽
debugMode = True # 调试模式，开启时不删除临时文件

def drawLetter(letter = 'A', base = 10): # 从文件中读取，并画出单个字母的验证码图像存储为数组
    with open('./fonts/' + letter + '.txt', 'r') as f:
        contentList = f.read().replace('[', '').replace(']', '').split(',')
    temp = []
    for num in range(len(contentList)):
        if num % 2 == 1:
            contentList[num] = int(contentList[num]) + base# + random.randint(-5, 5)
        else:
            contentList[num] = int(contentList[num]) + 15# + random.randint(-5, 5)
        temp.append(int(contentList[num]))
        if num % 2 == 1:
            lettersCover.append(temp)
            temp = []    

# 生成验证码
lettersList = ['A','B','C','D','E','F','G','H','J','K', 'M','N','R','T','V','W','X','Y']

# 排除了极可能容易被人类误认的字母，例如Z错认为2，I错认为1
# 字体文件存储在fonts目录下。构建自己的字体的方式：将单个字母的图片保存为detect.png，使用pic2np.py将其转换为detect.txt，重命名后放置于fonts目录下

code = random.choices(lettersList, k = 4) # 若更改长度，请计算并更改图片长度
print(code) # 输出验证码
baseLine = 20 # 首个字母距离左边框的距离
for letter in code:
    drawLetter(letter, baseLine)
    baseLine += 120 # 此处的baseLine被赋值为下一个字母距离左边框的距离，120为计算得出的最大字母宽度 + 20*2的间隔

status = False # 判断是否已存储验证码 COVER
saveRegion = [] # 保存的验证码 COVER 区域

# 生成文字的白噪声图像
def randomNoice(width, height):
    global status
    img = (np.random.rand(width, height, 1) * 255).astype(np.uint8) # 生成白噪声
    if not status: #没有存储 COVER
        for i in range(len(lettersCover)):
            saveRegion.append(img[lettersCover[i][0]][lettersCover[i][1]]) # 将首次图像的COVER区域保存
        status = True
    else: #已经存储 COVER
        for i in range(len(saveRegion)): # 将此处白噪声的COVER处替换为不变的图像
            if random.randint(0, 100) >= 35: # 增加损失，降低图像特征匹配风险
                img[lettersCover[i][0]][lettersCover[i][1]] = saveRegion[i]
    img = Image.fromarray(np.squeeze(img), mode = 'L') # 从array转为img
    return img

for i in range(0, fps): # 生成90帧图像
    randomNoice(height, width).save('./temp/random' + str(i) + '.jpg')

"""
with imageio.get_writer(uri = 'output.gif', mode = 'I', fps = 90) as writer:
    for i in range(90):
        writer.append_data(imageio.imread(f'random{i}.jpg'))
"""

images = []
for i in range(0, fps):
    images.append(imageio.imread(f'./temp/random{i}.jpg'))

filename = './outputs/output_' + str(time.time()) + '.gif'
imageio.mimsave(filename, images, duration=0, loop=0, fps=fps)

if not debugMode:
    shutil.rmtree('./temp')
    os.makedirs('./temp')