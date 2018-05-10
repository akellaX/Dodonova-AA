import json
import cv2
import numpy as np
import math
import random
from matplotlib import pyplot as plt
# библиотека используемая для нахождения точек пересечения между обЪектами
from shapely.geometry import LineString
import shapely.geometry as geometry


# JSON для чтения сегментации
def readJson(filename):
    json_data = open(filename).read()
    data = json.loads(json_data)
    objects = data["objects"]
    return objects


# метод для чтения полигона дороги из JSON
def getRoad(objects):
    for object in objects:
        if (object["label"] == "road"):
            road = object["polygon"]
            break
    return road


# метод для чтения полигонов машин
def getCars(objects):
    cars = []
    for object in objects:
        if (object["label"] == "car"):
            cars.append(object["polygon"])
    return cars


# метод для нахождения пересечения дороги и
# горизонтали на которую ставится машина
def findRoadIntersection(choosenHorizontal, objects, road_img):
    img_width = road_img.shape[1]
    road = getRoad(objects)
    ans = []
    line = LineString([(0, choosenHorizontal), (img_width, choosenHorizontal)])
    polygon = []
    for point in road:
        polygon.append((point[0], point[1]))

    poly = geometry.Polygon(polygon)
    point = str(poly.intersection(line))
    if (point != "GEOMETRYCOLLECTION EMPTY"):
        arr = point.split("(")[1]
        arr = arr.replace(")", "")
        arr = arr.replace(",", "")
        arr = arr.split(" ")
        point1 = (int(float(arr[0])), int(float(arr[1])))
        point2 = (int(float(arr[2])), int(float(arr[3])))
        # cv2.line(road_img, point1, point2, (0,0,255),2)

        # print(point1, point2)

        return point1[0], point2[0]
    else:
        print("No free road on this horizontal")
        return False


# выбор машины для масштабирования
def rectCar(objects, HORIZEN, road_img):
    params = []
    cars = getCars(objects)
    min_val = float('inf')
    min_index = 0
    for index in range(len(cars)):
        car = np.asarray(cars[index], np.int32)
        x, y, w, h = cv2.boundingRect(car)
        # print(abs(w / h - 1))
        if abs(w / h - 1) < min_val and x > 200 and x < 1800:
            min_index = index
            min_val = abs(w / h - 1)
    car = np.asarray(cars[min_index], np.int32)
    x, y, w, h = cv2.boundingRect(car)
    # print(min_index)

    distHoriz = y + h - HORIZEN
    car_width = w
    param = distHoriz / car_width
    params.append(param)
    cv2.rectangle(road_img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    drawHorizon(road_img)
    # print("param =", param)
    return param


# отрисовка линии горизонта - синяя линия на фото
def drawHorizon(road_img):
    img_height, img_width, img_channels = road_img.shape
    cv2.line(road_img, (0, 400), (img_width, 400), (200, 20, 20), 5)


# масштабирование машины
def getPerspectCar(param, horizontal, HORIZEN, car_img):
    h, w, channels = car_img.shape
    dist = horizontal - HORIZEN
    width = dist / param
    car_img_small = cv2.resize(car_img, (0, 0), fx=width / w, fy=width / w)

    return car_img_small


def getPerspectCarMath(param, car_img):
    h, w, channels = car_img.shape
    car_img_small = cv2.resize(car_img, (0, 0), fx=param / w, fy=param / w)

    return car_img_small


# клахи и размытие
def blurclahe(image):
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    lab = cv2.cvtColor(blur, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0)
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    blur = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return blur


def getRealDistance(alpha, h, heigh, car_heihg):
    distance = h * math.tan(math.pi/2-(car_heihg * alpha / (heigh * 2)))

    return distance


def getAlpha(fy, height):
    return 2 * math.atan(height / (2 * fy))


def getSizeOfCar(f, real_width, distance):
    return real_width * f / distance


# вклейка машины в дорожную сцену
def drawCarOtherCars(jsonFileName, carImg, roadImg, horizontal):
    np.set_printoptions(threshold=np.nan)
    # чтение изображений машины и дорожной сцены
    car_img = cv2.imread(carImg, cv2.IMREAD_UNCHANGED)
    road_img = cv2.imread(roadImg, cv2.IMREAD_UNCHANGED)
    # переменная проставляющая  x для линии горизонта
    HORIZEN = 400
    objects = readJson(jsonFileName)
    param = rectCar(objects, HORIZEN, road_img)
    car_img = getPerspectCar(param, horizontal, HORIZEN, car_img)
    x1, x2 = findRoadIntersection(horizontal, objects, road_img)
    # x_offset = random.randint(x1, x2)
    x_offset = 900
    y_offset = horizontal - car_img.shape[0]

    y1, y2 = y_offset, y_offset + car_img.shape[0]
    x1, x2 = x_offset, x_offset + car_img.shape[1]

    alpha_s = car_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        road_img[y1:y2, x1:x2, c] = (alpha_s * car_img[:, :, c] + alpha_l * road_img[y1:y2, x1:x2, c])

    return blurclahe(road_img)


def drawCarMath(jsonFileName, carImg, roadImg, horizontal, f, fy):
    np.set_printoptions(threshold=np.nan)
    # чтение изображений машины и дорожной сцены
    car_img = cv2.imread(carImg, cv2.IMREAD_UNCHANGED)
    road_img = cv2.imread(roadImg, cv2.IMREAD_UNCHANGED)
    # переменная проставляющая  x для линии горизонта
    HORIZEN = 400
    objects = readJson(jsonFileName)
    param = rectCar(objects, HORIZEN, road_img)
    height = 1024
    alpha = getAlpha(fy, height)
    distance = getRealDistance(alpha, 1.22, height, horizontal)
    sizeOfCar = getSizeOfCar(f, 2.5, distance)

    car_img = getPerspectCarMath(sizeOfCar, car_img)
    x1, x2 = findRoadIntersection(horizontal, objects, road_img)
    # x_offset = random.randint(x1, x2)
    x_offset = 900
    y_offset = horizontal - car_img.shape[0]

    y1, y2 = y_offset, y_offset + car_img.shape[0]
    x1, x2 = x_offset, x_offset + car_img.shape[1]

    alpha_s = car_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        road_img[y1:y2, x1:x2, c] = (alpha_s * car_img[:, :, c] + alpha_l * road_img[y1:y2, x1:x2, c])

    return blurclahe(road_img)


def toRGB(img):
    b, g, r = cv2.split(img)
    image_RGB = cv2.merge((r, g, b))
    return image_RGB


# __main__
jsonFile = "car_proj/frankfurt_3.json"
carImg = "car_proj/back_view.png"
roadImg = "car_proj/frankfurt_3.png"
roadCar = drawCarOtherCars(jsonFile, carImg, roadImg, 500)
roadMath = drawCarMath(jsonFile, carImg, roadImg, 500, 1200, 2265)
cv2.imshow("test.jpeg", roadCar)
cv2.waitKey(100000)
cv2.imshow("test.jpeg", roadMath)
# road = toRGB(road)
# plt.imshow(road)
cv2.waitKey(100000)
