import cv2
import json_parser as jp
import numpy as np
import math
import random

from shapely.geometry import LineString
import shapely.geometry as geometry

HORIZEN = 400
horizontal = 600

GREEN = (33, 204, 41)


def toBGR(img):
    b, g, r, a = cv2.split(img)
    image_BGR = cv2.merge((b, g, r))
    return (image_BGR, a)


np.set_printoptions(threshold=np.nan)
car_img = cv2.imread("car_proj\\back_view.png", cv2.IMREAD_UNCHANGED)
road_img = cv2.imread("car_proj\\frankfurt.png", cv2.IMREAD_UNCHANGED)
alpha = cv2.imread("123.png", cv2.IMREAD_UNCHANGED)


# road_BGR, road_a = toBGR(road_img)

def fillPoly(road):
    road = np.asarray(road, np.int32)
    cv2.fillPoly(road_img, [road], GREEN)

    cv2.imshow("image", road_img)
    cv2.waitKey(100000)

def findRoadIntersection(choosenHorizontal):
    img_width= road_img.shape[1]
    road = jp.getRoad()
    ans = []
    line = LineString([(0, choosenHorizontal),(img_width, choosenHorizontal)])
    polygon = []
    for point in road:
        polygon.append((point[0], point[1]))

    poly = geometry.Polygon(polygon)
    point = str(poly.intersection(line))
    if (point != "GEOMETRYCOLLECTION EMPTY"):
        arr = point.split("(")[1]
        arr = arr.replace(")","")
        arr = arr.replace(",", "")
        arr = arr.split(" ")
        point1 = (int(float(arr[0])), int(float(arr[1])))
        point2 = (int(float(arr[2])), int(float(arr[3])))
        # cv2.line(road_img, point1, point2, (0,0,255),2)

        print(point1, point2)

        return point1[0], point2[0]
    else:
        print("No free road on this horizontal")
        return False
def rectCar():
    params = []
    cars = jp.getCars()
    # for car in cars:
    #     car = np.asarray(car,np.int32)
    #     x, y, w, h = cv2.boundingRect(car)
    #     distHoriz = y+h-HORIZEN
    #     car_width = w
    #     param = distHoriz/car_width
    #     params.append(param)
    #     cv2.rectangle(road_img,(x,y), (x+w,y+h), (0,255,0), 1)
    car = np.asarray(cars[0], np.int32)
    x, y, w, h = cv2.boundingRect(car)
    distHoriz = y + h - HORIZEN
    car_width = w
    param = distHoriz / car_width
    params.append(param)
    cv2.rectangle(road_img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    drawHorizon()
    print("param =",param)
    return param
    # print(np.sum(params)/len(params))
    # cv2.imshow("road", road_img)
    # cv2.waitKey(1000000)


def drawHorizon():
    img_height, img_width, img_channels = road_img.shape
    cv2.line(road_img, (0, 400), (img_width, 400), (200, 20, 20), 5)

def getPerspectCar(param):
    h, w, channels = car_img.shape
    dist = horizontal-HORIZEN
    width = dist / param
    car_img_small = cv2.resize(car_img, (0, 0), fx=width / w, fy=width / w)
    # hh, ww, cc = car_img_small.shape
    # cv2.rectangle(road_img, (250, horizontal), (250 + ww, horizontal + hh), (0, 0, 255), 1)

    return car_img_small


def drawCar():

    param = rectCar()
    car_img = getPerspectCar(param)
    x1, x2 = findRoadIntersection(horizontal)
    x_offset = random.randint(x1, x2)
    y_offset = horizontal - car_img.shape[0]

    y1, y2 = y_offset, y_offset + car_img.shape[0]
    x1, x2 = x_offset, x_offset + car_img.shape[1]

    alpha_s = car_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        road_img[y1:y2, x1:x2, c] = (alpha_s * car_img[:, :, c] + alpha_l * road_img[y1:y2, x1:x2, c])


# cv2.line(road_img, (point[0][0],point[0][1]), (point[1][0],point[1][1]), GREEN, 2)
drawCar()

cv2.imshow("image", road_img)
cv2.waitKey(100000)
