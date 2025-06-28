# 导入所需的库
import numpy as np
import cv2
import matplotlib.pyplot as plt

# 将两个输入图像读取为灰度图像
img1 = cv2.imread('./random0.jpg',0)
img2 = cv2.imread('./random1.jpg',0)

# 初始化 SIFT 检测器
sift = cv2.SIFT_create()

# 检测和计算具有 SIFT 的关键点和描述符
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# 创建 BFMatcher 对象
bf = cv2.BFMatcher()

# 匹配描述符。
matches = bf.match(des1,des2)

# 基于距离对匹配项进行排序
matches = sorted(matches, key=lambda val: val.distance)

# 绘制前50个匹配项。
out = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2)
plt.imshow(out), plt.show()
