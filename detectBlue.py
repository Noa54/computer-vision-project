import numpy as np 
import cv2 
from PIL import Image

def get_limits(color):
    c = np.uint8([[color]]) #converts input color into numpy array that opencv requires
    
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV) #converts from bgr to hsv for detection in any lighting

    hue = hsvC[0][0][0]

    lower_hue = max(0, hue - 15)
    upper_hue = min(180, hue + 15)

    lowerLimit = np.array([lower_hue, 30, 20], dtype=np.uint8)
    upperLimit = np.array([upper_hue, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit




blue = [255, 0, 0] #what colour you want detected in BGR

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    if not ret:
        print("Failed to get the video, status false")
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=blue)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 5)


    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()

cv2.destroyAllWindows()
