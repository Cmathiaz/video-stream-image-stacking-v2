
video stream image stacking v2 -- live version

A very simple streamed video image stacking code!

Version 2.1

left mouse click to select a small region for real-time averaging.
Stacked photo appears is another live widow that can be zoomed or
resized. right mouse click pauses averaging. left mouse click selects
a region and starts again. press q to abort.

improves statistical camera noise (and the resolution a little) by stacking
many images captured from an rtsp protocol security camera.

no frame to frame ECC motion vector estimation done here, only simple stacking
and averaging! The built-in 3D noise reduction available in most cameras
averages only over smaller number of frames. but it is done in real time

a final stacked output image is produced after averaging the frames.
press q in the displayed video window to abort during frame capture.

resolution improvements are only marginal. Noise improvement is better.
if there is any movement in the field of view, it will get blurred.
Works correctly only if there is no movement.

developed this simple python code using Pycharm in an M1 Macbook Air.

C. Mathiazhagan, IIT Madras
