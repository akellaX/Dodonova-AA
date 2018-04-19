import json
import numpy as np
import cv2

json_data = open("car_proj\\frankfurt.json").read()
data = json.loads(json_data)
objects = data["objects"]
img = np.zeros((1024, 2048, 3), np.uint8)
img.fill(255)
def getRoad():
    for object in objects:
        if (object["label"]=="road"):
            road = object["polygon"]
            break;
    # sky = np.asarray(sky,np.int32)
    # cv2.fillPoly(img, [sky], (255,181,107))
    # road = np.asarray(road,np.int32)
    # cv2.fillPoly(img, [road], (0,0,0))

    return road;

def getCars():
    cars = []
    for object in objects:
        if (object["label"]=="car"):
            cars.append(object["polygon"]);

    return cars