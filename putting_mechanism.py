import cv2
import json_parser as jp
import numpy as np

car_img = cv2.imread("C:\\Users\\User\\Desktop\\car_proj\\back_view.png",cv2.IMREAD_UNCHANGED)
road_img = cv2.imread("C:\\Users\\User\\Desktop\\car_proj\\hanover_color.png",cv2.IMREAD_UNCHANGED)


def alphaMerge(img):
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50  # creating a dummy alpha channel image.
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    return img_BGRA

def fillPoly(road):
    h = 500;
    w = 500;
    color = (66,80,244)
    img = np.zeros((1024,2048,3),np.uint8)
    road = np.asarray(road,np.int32)
    cv2.fillPoly(img, [road], (255,255,255))

    cv2.imshow("image",img)
    cv2.waitKey(100000)


# cv2.rectangle(road_img,(384,0),(510,128),(0,255,0),-1)
# x_offset=y_offset=500
# road_img[y_offset:y_offset+car_img.shape[0], x_offset:x_offset+car_img.shape[1]] = car_img
# cv2.imshow("image",road_img)
# cv2.waitKey(10000)
fillPoly(jp.getRoad())