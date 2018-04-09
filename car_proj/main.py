import cv2

car_img = cv2.imread("road.jpg",cv2.IMREAD_UNCHANGED)
cv2.imshow("imgae",car_img)
cv2.waitKey(10000)