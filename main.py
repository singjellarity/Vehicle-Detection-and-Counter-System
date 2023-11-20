#import necessary libraries
import cv2 #openCV
import numpy as np
from time import sleep

#state the required rectangle size
width_min = 40
height_min = 40
offset = 3
pos_line = 325 

# FPS to vídeo
delay = 60

detec = []
cars = 0

#how to compute for the center of the cars	
def peg_center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


# video source input
cap = cv2.VideoCapture('FINAL.mp4')
#video taken from overpass at Aurora Blvd. corner Hemady street

#use subract to remove the background from the video
subtract = cv2.bgsegm.createBackgroundSubtractorMOG()


while True:
    ret, frame1 = cap.read() #read the input per frame
    tempo = float(1/delay)
    sleep(tempo) 
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) #transform frame to gray
    blur = cv2.GaussianBlur(grey, (3, 3), 5) #blur the frame
    img_sub = subtract.apply(blur)
    dilate = cv2.dilate(img_sub, np.ones((5,5))) #morph the features of the frame by using dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

    # The morphologyEx() of the method of the class Imgproc accepts src, dst, op, kernel as parameters
    dil = cv2.morphologyEx(dilate, cv2. MORPH_CLOSE, kernel)
    dil = cv2.morphologyEx(dil, cv2. MORPH_CLOSE, kernel)

    # OpenCV has findContour() function that helps in extracting the contours from the image.
    # It works best on binary images, so we should first apply thresholding techniques, Sobel edges, etc.
    contour, h = cv2.findContours(dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    # it will create a line
    cv2.line(frame1, (25,pos_line), (935, pos_line), (176, 130, 39), 1)
    for(i, c) in enumerate(contour):
        (x, y, w, h) = cv2.boundingRect(c)
        validar_contorno = (w >= width_min) and (h >= height_min)
        if not validar_contorno:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 1)
        centro = peg_center(x, y, w, h)
        detec.append(centro)
        cv2.circle(frame1, centro, 1, (0, 0, 255), 1)

        for (x, y) in detec:
            if (y < (pos_line + offset)) and (y > (pos_line-offset)):
                cars += 1
                cv2.line(frame1, (25,pos_line), (935, pos_line ), (0, 127, 255), 3)
                detec.remove((x, y))
                print("No. of cars detected : " + str(cars))

    # cv2.putText() method is used to draw a text string on any image.
    # Parameters: image, text, org(coordinate), font, color, thickness
    cv2.putText(frame1, "VEHICLE COUNT : "+str(cars), (100, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 1)
    cv2.imshow("Video Original", frame1)
    cv2.imshow(" Detection ", dil)

    # To display the image, you can use the imshow() method of cv2
    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows()
cap.release()
