import numpy as np
import cv2

def getRealCoords(pixelCoords, cameraMat):
    invCameraMat = np.linalg.inv(cameraMat)
    realCoords = np.dot(invCameraMat, pixelCoords)
    return realCoords

pixelCoords = np.array([[400],[400],[1]])
cameraMat = np.array([[2268,0,1048],[0,2225,519],[0,0,1]])

print(getRealCoords(pixelCoords, cameraMat))