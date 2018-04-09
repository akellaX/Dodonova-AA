import cv2
import json_parser as jp
import numpy as np
from matplotlib import pyplot as plt

def toBGR(img):
    b, g, r, a = cv2.split(img)
    image_BGR = cv2.merge((b, g, r))
    return (image_BGR, a)

np.set_printoptions(threshold=np.nan)
car_img = cv2.imread("C:\\Users\\User\\Desktop\\car_proj\\back_view.png",cv2.IMREAD_UNCHANGED)
road_img = cv2.imread("C:\\Users\\User\\Desktop\\car_proj\\hanover_color.png",cv2.IMREAD_UNCHANGED)
alpha = cv2.imread("123.png",cv2.IMREAD_UNCHANGED)

road_BGR, road_a = toBGR(road_img)

def fillPoly(road):
    h = 500;
    w = 500;
    color = (66,80,244)
    img = np.zeros((1024,2048,3),np.uint8)
    road = np.asarray(road,np.int32)
    cv2.fillPoly(img, [road], (255,255,255))

    cv2.imshow("image",img)
    cv2.waitKey(100000)


x_offset=y_offset=500


y1, y2 = y_offset, y_offset + car_img.shape[0]
x1, x2 = x_offset, x_offset + car_img.shape[1]

alpha_s = car_img[:, :, 3] / 255.0
alpha_l = 1.0 - alpha_s

for c in range(0, 3):
    road_BGR[y1:y2, x1:x2, c] = (alpha_s * car_img[:, :, c] + alpha_l * road_BGR[y1:y2, x1:x2, c])

# road_BGR[y_offset:y_offset+car.shape[0], x_offset:x_offset+car.shape[1]] = car
cv2.imshow("image",road_BGR)
cv2.waitKey(10000)
# fillPoly(jp.getRoad())