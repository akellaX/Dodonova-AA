import json
import numpy as np
import cv2
def getRoad():
    img = np.zeros((1024,2048,3), np.uint8)
    img.fill(255)
    json_data = open("C:\\Users\\User\\Desktop\\car_proj\\hanover.json").read()
    data = json.loads(json_data)
    objects = data["objects"]
    sky = objects[0]["polygon"];
    for object in objects:
        if (object["label"]=="road"):
            road = object["polygon"]
            break;
    # sky = np.asarray(sky,np.int32)
    # cv2.fillPoly(img, [sky], (255,181,107))
    # road = np.asarray(road,np.int32)
    # cv2.fillPoly(img, [road], (0,0,0))
    # cv2.imshow("IMAGE",img)
    # cv2.waitKey(10000)
    return road;