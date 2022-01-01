# A very simple streamed video image stacking code!
#
# Version 2.1
# left mouse click to select a small region for real-time averaging.
# Stacked photo appears is another live widow that can be zoomed or
# resized. right mouse click pauses averaging. left mouse click selects
# a region and starts again. press q to abort.
#
# improves statistical camera noise (and the resolution a little) by stacking
# many images captured from an rtsp protocol security camera.
#
# no frame to frame ECC motion vector estimation done here, only simple stacking
# and averaging! The built-in 3D noise reduction available in most cameras
# averages only over smaller number of frames. but it is done in real time
#
# a final stacked output image is produced after averaging the frames.
# press q in the displayed video window to abort during frame capture.
#
# resolution improvements are only marginal. Noise improvement is better.
# if there is any movement in the field of view, it will get blurred.
# Works correctly only if there is no movement.
#
# developed this simple python code using Pycharm in an M1 Macbook Air.
#
# C. Mathiazhagan, IIT Madras

import cv2
import numpy as np
import matplotlib.pyplot as plt

username = 'admin'  # usually the default username is admin
password = 'password'  # enter the password string here
ipaddress = '192.168.0.50'  # enter the ip address of the camera, use DHCP in
# your wifi router to hardwire it to some permanent value
portnumber = '554'  # rtsp video stream port address

H = 0
W = 0
Ch = 0
nframes = 25*60  # number of frames for averaging, 25 is the typical fps

# Create the circle
colour = (0, 0, 255)
lineWidth = 2  # -1 will result in filled circle
point1 = (10, 10)
point2 = (20, 20)
p20 = 0  # point2 is a tuple that can't be modified
p21 = 0
windowH = 100
windowW = 200
Pressed = False

# function for detecting left mouse click


def click(event, x, y, flags, param):
    global point1, point2, p20, p21, Pressed

    if event == cv2.EVENT_LBUTTONDOWN:
        print("Pressed L down", x, y)
        point1 = (x, y)
        Pressed = False

    if event == cv2.EVENT_LBUTTONUP:
        print("Pressed L up", x, y)
        p20 = point1[0] + windowW
        p21 = point1[1] + windowH
        if p20 > W:  # check limits
            p20 = W
        if p21 > H:
            p21 = H
        point2 = (p20, p21)  # assign now as a tuple
        Pressed = True

    if event == cv2.EVENT_RBUTTONDOWN:
        Pressed = False
        print('stacking paused, left click to start again')

# mouse event handler


cv2.namedWindow("Capturing")
cv2.setMouseCallback("Capturing", click)

nph = 0  # photo number

print("Before URL")  # for checking

# look up correct rtsp address, it usually goes like these
# cap = cv2.VideoCapture('rtsp://admin:password@192.168.0.50:554')
# cap = cv2.VideoCapture('rtsp://admin:password@192.168.0.50')

# for special Imou cameras, LOOC 2, Ranger 2, Cue 2, this is the correct rtsp string!
# check this website: https://www.ispyconnect.com/camera/imou
# cap = cv2.VideoCapture('rtsp://admin:password@192.168.0.51/cam/realmonitor?channel=1&subtype=00&authbasic=YWRtaW46YWRtaW4=')

cap = cv2.VideoCapture('rtsp://' + username + ':' + password + '@' + ipaddress + ':'
                       + portnumber + '/cam/realmonitor?channel=1&subtype=00')

print("After URL")  # if you see this, the camera is streaming correctly!

ret, frame = cap.read()  # capture read

if not ret:
    print('not able to capture the stream!')
    exit()

# initialize some empty arrays for use
img = np.zeros(frame.shape, np.uint8)
imgBGR = np.zeros((windowH, windowW, 3), np.uint32)
imgFinal = np.zeros(frame.shape, np.uint32)
H, W, Ch = img.shape  # get height, width and channel sizes

while nph < 30000:  # just loop over a large number. press q to quit

    count = 0  # frame count
    imgBGR = np.zeros((windowH, windowW, 3), np.uint32)

# capture nframes and loop again , camera fps is usually 25 frames per second
# so the capture time is 4 seconds

    while count < nframes:  # number of frames for averaging

        ret, frame = cap.read()
        # copy frame to image for manipulation
        img = frame  # copy frame to image, not necessary, wasted some memory here

        if Pressed:  # left mouse pressed
            cv2.rectangle(img, point1, point2, colour, lineWidth)  # draw rectangle
            count = count + 1  # count number of frames
            imgBGR[0: point2[1] - point1[1], 0 : point2[0] - point1[0], :] += img[point1[1]: point2[1],\
                                         point1[0]:point2[0], :]  # stack images by adding and accumulating BGR

        cv2.imshow("Capturing", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to abort while capturing
            quit()

    imgFinal = np.uint8(imgBGR / count)  # find average and recast to integers
    print('captured frame H, W and Ch; nph; nframes =', H, W, Ch, nph, nframes)

    cv2.imshow("live stacked photo", imgFinal)
    nph = nph+1

# capture done now
cap.release()
cv2.destroyAllWindows()