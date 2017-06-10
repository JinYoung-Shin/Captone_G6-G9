import numpy as np
import cv2
import math

webcam = cv2.VideoCapture(0)

if webcam.isOpened():  # try to get the first frame
    rval, image = webcam.read()
else:
    rval = False

# define the list of acceptable colors
colors = [([0,133,77], [255, 173, 127])]
blue =[([110,50,50]),[130,255,255]]


while rval:
    # loop over the boundaries
    for (lower, upper) in colors:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        imgg = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(imgg, lower, upper)
        output = cv2.bitwise_and(imgg, imgg, mask=mask)

    rval, image = webcam.read()
    edges = cv2.Canny(output, 30, 30, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    img = cv2.medianBlur(image, 15)
    imgg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(imgg, cv2.HOUGH_GRADIENT, 1, 10,
                               param1=40, param2=40, minRadius=10, maxRadius=100)


    if circles != None:
        for i in circles[0, :]:
        # draw the outer circle
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(image, (i[0], i[1]), 2, (255, 0, 0), 3)

    if lines != None:
        for x in range(0, 1):
            for rho, theta in lines[x]:
                x1 = int(np.cos(theta) * rho + 1000 * (-np.sin(theta)))
                y1 = int(np.sin(theta) * rho + 1000 * np.cos(theta))
                x2 = int(np.cos(theta) * rho - 1000 * (-np.sin(theta)))
                y2 = int(np.sin(theta) * rho - 1000 * np.cos(theta))
                cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 1)
                cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)

    cv2.imshow("images", np.hstack([image, output]))
    key = cv2.waitKey(20)

    if key in [27, ord('Q'), ord('q')]:  # exit on ESC(q)
        # Exception for no line or circle
        if lines != None and circles != None:
            cv2.destroyWindow("images")
            break
        else:
            print("circle or line is not detected")


img = cv2.medianBlur(image, 15)
imgg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
circles = cv2.HoughCircles(imgg, cv2.HOUGH_GRADIENT, 1, 10,
                               param1=50, param2=40, minRadius=0, maxRadius=100)
for x in range(0, 1):
           for rho, theta in lines[x]:
               x1 = int(np.cos(theta) * rho + 1000 * (-np.sin(theta)))
               y1 = int(np.sin(theta) * rho + 1000 * np.cos(theta))
               x2 = int(np.cos(theta) * rho - 1000 * (-np.sin(theta)))
               y2 = int(np.sin(theta) * rho - 1000 * np.cos(theta))
               cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 1)
               cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)

               y1 = -1 * y1
               y2 = -1 * y2
               a = (y2 - y1) / (x2 - x1)

d = [1000, 1000, 1000, 1000, 1000, 1000]
j = 0

dex =0;

for i in circles[0,:]:
    # draw the outer circle
        if dex < 5:
            cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
            print(i[0],i[1])
        # draw the center of the circle
            cv2.circle(image,(i[0],i[1]),2,(255,0,0),3)
            i[1] = -1 * i[1]
            d[j]= abs(a*(i[0]-x1) + y1 -i[1]) / (math.sqrt(a*a +1))
            j = j+1
            dex = dex +1

print(d)
print("d = ",min(d))
j =0
for i in d :
    if min(d) == i:
        mi = j
    j = j+1
print("index :",mi)

print(circles[0,mi][0],circles[0,mi][1])

cv2.imshow('Edges', image)
cv2.imshow('Output', output)
cv2.waitKey()