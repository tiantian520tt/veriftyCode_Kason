import numpy as np
from PIL import Image
np.set_printoptions(threshold=np.inf)
image = Image.open('detect.png')

numpydate = np.asarray(image)
gray_img = np.dot(numpydate[...,:1], [1]).astype(np.uint8)

recorder = []
minX = 10000
minY = 10000
for i in range(len(gray_img)):
    for j in range(len(gray_img[i])):
        if gray_img[i][j] != 255:
            recorder.append([i, j])
            minX = min(i, minX)
            minY = min(j, minY)

for u in range(len(recorder)):
    recorder[u][0] -= minX
    recorder[u][1] -= minY
with open("detect.txt",'w') as f:
    f.write(str(recorder))