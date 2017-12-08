import numpy as np
import cv2
import math
import pygame
import time
import copy
import speech_recognition as sr



#
# while True:
#
#     pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
#     bang = pygame.mixer.Sound('order.wav')
#     bang.play()
#     time.sleep(bang.get_length())
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Say something!")
#
#
#         audio = r.listen(source)
#
#    # tmp = r.recognize_google(audio)
#
#
#     try :
#        # print(tmp)
#         print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
#         if r.recognize_google(audio) == "hello":
#          break
#
#     except sr.UnknownValueError:
#         pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
#         bang = pygame.mixer.Sound('again.wav')
#         bang.play()
#         time.sleep(bang.get_length())
#
#     except sr.RequestError as e:
#         pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
#         bang = pygame.mixer.Sound('again.wav')
#         bang.play()
#         time.sleep(bang.get_length())
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))

pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
bang = pygame.mixer.Sound('ready.wav')
bang.play()
time.sleep(bang.get_length())

webcam = cv2.VideoCapture(0)

#sig = 0


if webcam.isOpened() :  # try to get the first frame
    rval, image = webcam.read()
else:
    rval = False

# define the list of acceptable colors
colors = [([0,133,77], [255, 173, 127])]

#colors = [([110, 100, 100], [130, 255, 255])]


while rval:
    # loop over the boundaries
    for (lower, upper) in colors:
        #s   create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        imgg = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(imgg, lower, upper)
        output = cv2.bitwise_and(imgg, imgg, mask=mask) #output = cv2.bitwise_and(imgg, imgg, mask=mask)
        #output2 = cv2.cvtColor(output, cv2.COLOR_BGR2YCrCb)
        #cv2.circle(output, (100, 100), 50, (0, 255, 0), 2)
       # j =image.getpixel((100, 100))
        # show the images
    # for (lower2, upper2) in colors:
    #     # s   create NumPy arrays from the boundaries
    #     lower2 = np.array(lower2, dtype="uint8")
    #     upper2 = np.array(upper2, dtype="uint8")
    #     imgg = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    #     # find the colors within the specified boundaries and apply
    #     # the mask
    #     mask = cv2.inRange(image, lower, upper)
    #     output = cv2.bitwise_and(imgg, imgg, mask=mask)  # output = cv2.bitwise_and(imgg, imgg, mask=mask)
    #     output2 = cv2.cvtColor(output, cv2.COLOR_BGR2YCrCb)




    rval, image = webcam.read()
    edges = cv2.Canny(output, 30, 30, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    image2 = copy.copy(image)
    #image2 = image
    img = cv2.medianBlur(image, 15)
    imgg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#    imga = cv2.medianBlur(output2, 15)

   # imgga = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(imgg, cv2.HOUGH_GRADIENT, 1, 5,
                               param1=50, param2=30, minRadius=0, maxRadius=15)
    if circles != None:
        index = 0
        for i in circles[0, :]:
        # draw the outer circle
            if index  < 2 :
                cv2.circle(image2, (i[0], i[1]), i[2], (0, 255, 0), 2)
                print(i[0],i[1])
                #cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # print(circles[0,0])

            # draw the center of the circle
                cv2.circle(image2, (i[0], i[1]), 2, (0, 0, 255), 3)
                #cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
                index = index +1

    if lines != None:
        index2 = 0
        for x in range(0, 1):
            if ( index2 <3):
             for rho, theta in lines[x]:
                x1 = int(np.cos(theta) * rho + 1000 * (-np.sin(theta)))
                y1 = int(np.sin(theta) * rho + 1000 * np.cos(theta))
                x2 = int(np.cos(theta) * rho - 1000 * (-np.sin(theta)))
                y2 = int(np.sin(theta) * rho - 1000 * np.cos(theta))
                cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 1)
                cv2.line(image2, (x1, y1), (x2, y2), (0, 0, 255), 1)
                index2 = index2 +1

    cv2.imshow("images", np.hstack([image2, output])) #output
    cv2.imshow("tes ", edges)
#    cv2.imshow("test",imga)


    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Say something!")
    #
    #     audio = r.listen(source)
    #
    # try:
    #         # print(tmp)
    #         print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    #
    # except sr.UnknownValueError:
    #         pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
    #         bang = pygame.mixer.Sound('again.wav')
    #         bang.play()
    #         time.sleep(bang.get_length())
    #         continue
    #
    # except sr.RequestError as e:
    #         pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
    #         bang = pygame.mixer.Sound('again.wav')
    #         bang.play()
    #         time.sleep(bang.get_length())
    #         print("Could not request results from Google Speech Recognition service; {0}".format(e))
    #         continue
    #
    # if r.recognize_google(audio) == "this":
    #             if lines != None and circles != None:
    #                 pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
    #                 bang = pygame.mixer.Sound('yes.wav')
    #                 bang.play()
    #                 time.sleep(bang.get_length())
    #                 break;
    #
    #             if lines != None and circles == None:
    #                 pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
    #                 bang = pygame.mixer.Sound('bolt.wav')
    #                 bang.play()
    #                 time.sleep(bang.get_length())
    #             if circles != None and lines == None:
    #                 pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
    #                 bang = pygame.mixer.Sound('position.wav')
    #                 bang.play()
    #                 time.sleep(bang.get_length())


    key = cv2.waitKey(20)
    if key in [27, ord('Q'), ord('q')]:  # exit on ESC
        if lines != None and circles != None:
            pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
            bang = pygame.mixer.Sound('yes.wav')
            bang.play()
            time.sleep(bang.get_length())
            break;

        if lines != None and circles ==None:
            pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
            bang = pygame.mixer.Sound('bolt.wav')
            bang.play()
            time.sleep(bang.get_length())
        if circles != None and lines ==None:
            pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
            bang = pygame.mixer.Sound('position.wav')
            bang.play()
            time.sleep(bang.get_length())






# imga = cv2.medianBlur(output2, 15)
#
# imgga = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
# circles = cv2.HoughCircles(imgga, cv2.HOUGH_GRADIENT, 1, 5,
#                                param1=50, param2=30, minRadius=0, maxRadius=100)





# circles = cv2.HoughCircles(imgg, cv2.HOUGH_GRADIENT, 1, 10,
#                                param1=50, param2=30, minRadius=0, maxRadius=30)
for x in range(0, 1):
           for rho, theta in lines[x]:
               x1 = int(np.cos(theta) * rho + 1000 * (-np.sin(theta)))
               y1 = int(np.sin(theta) * rho + 1000 * np.cos(theta))
               x2 = int(np.cos(theta) * rho - 1000 * (-np.sin(theta)))
               y2 = int(np.sin(theta) * rho - 1000 * np.cos(theta))
               cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 1)
               #cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)

               y1 = -1 * y1
               y2 = -1 * y2
               a = (y2 - y1) / (x2 - x1)

               #print(x1, y1)
               #print(x2, y2)
               #print(a)

d = [4000, 4000, 4000, 4000, 4000]
j = 0

dex =0;

for i in circles[0,:]:
    # draw the outer circle
        if dex < 2:
            cv2.circle(image2,(i[0],i[1]),i[2],(0,255,0),2)
        #print(circles[0,0])
            print(i[0],i[1])
    # draw the center of the circle
            cv2.circle(image2,(i[0],i[1]),2,(0,0,255),3)
            i[1] = -1 * i[1]
            d[j]= abs(a*(i[0]-x1) + y1 -i[1]) / (math.sqrt(a*a +1))
            j = j+1
            dex = dex +1
print (d)


print("d = ",min(d))

j =0
for i in d :
    if min(d) == i:
        mi = j
    j = j+1
print("index :",mi)

print(circles[0,mi][0],circles[0,mi][1])

cv2.imshow('Edges', image2)
cv2.imshow('Output', output)
#cv2.imshow('Mask',mask)
#cv2.imshow('Output',output)
cv2.waitKey()