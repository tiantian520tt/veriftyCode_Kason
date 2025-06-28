import random
import numpy as np
from PIL import Image
import imageio

lettersCover = []

def drawLetter(letter = 'A', base = 10):
    with open(letter + '.txt', 'r') as f:
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
code = random.choices(lettersList, k = 4)
print(code)
baseLine = 20
for letter in code:
    drawLetter(letter, baseLine)
    baseLine += 120

status = False
frozenCode = [0][0] * 100000
saveRegion = []

# 生成文字的白噪声图像
def randomNoice(width, height):
    global frozenCode, status
    img = (np.random.rand(width, height, 1) * 255).astype(np.uint8)
    if not status:
        for i in range(len(lettersCover)):
            saveRegion.append(img[lettersCover[i][0]][lettersCover[i][1]])
        status = True
    else:
        for i in range(len(saveRegion)):
            if random.randint(0, 100) >= 35: # 增加损失，降低图像特征匹配风险
                img[lettersCover[i][0]][lettersCover[i][1]] = saveRegion[i]
    img = Image.fromarray(np.squeeze(img), mode = 'L')
    return img

for i in range(0, 90):
    randomNoice(100, 500).save('random' + str(i) + '.jpg')


#with imageio.get_writer(uri = 'output.gif', mode = 'I', fps = 90) as writer:
#    for i in range(15):
#        writer.append_data(imageio.imread(f'random{i}.jpg'))

images = []
for i in range(0, 90):
    images.append(imageio.imread(f'random{i}.jpg'))

imageio.mimsave("output.gif", images, duration=0, loop=0, fps=90)
