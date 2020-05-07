import cv2
import numpy as np

'''
Virtual paint allows a user to draw on their screen simply
by holding a red object and moving it around.

Author: Anuj Patel
'''

'''
function to show live feed from camera and handle 
key presses and movement on the screen
'''


def showCamera(sliders):
    video = cv2.VideoCapture(0)
    first = None
    points = []
    cv2.namedWindow("Capture")
    cv2.moveWindow("Capture", 1, 1)
    sliders.create_sliders()

    drawing = True

    while True:
        _, img = video.read()
        masked = mask(img)
        color = sliders.get_color()

        if first is None:
            first = masked

        delta = cv2.absdiff(first, masked)

        if drawing:
            x, y = locate(delta)
            if x != 0 and y != 0:
                points.append([x, y, color])

        img = draw(points, img)
        img = cv2.flip(img, 1)

        cv2.imshow("Capture", img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        elif key == ord('c'):
            points = []

        elif key == ord('1'):
            sliders.set_color((0, 0, 255))

        elif key == ord('2'):
            sliders.set_color((0, 127, 255))

        elif key == ord('3'):
            sliders.set_color((0, 255, 255))

        elif key == ord('4'):
            sliders.set_color((0, 255, 0))

        elif key == ord('5'):
            sliders.set_color((255, 255, 0))

        elif key == ord('6'):
            sliders.set_color((255, 25, 0))

        elif key == ord('7'):
            sliders.set_color((255, 0, 255))

        elif key == ord('8'):
            sliders.set_color((0, 0, 0))

        elif key == ord('9'):
            sliders.set_color((255, 255, 255))

        elif key == ord(' '):
            drawing = not drawing
            points.append([-1, -1, None])


'''
function that takes an image as an input and returns
a masked grayscale image where any part of the original
image that had red will show up as white and everything
else will be black
'''


def mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([161, 155, 84])
    upper_red = np.array([179, 255, 255])
    masked = cv2.inRange(hsv, lower_red, upper_red)
    return masked


'''
function to detect movement between two images. Takes 
in a delta image image which will display differences
of two image pixels. Then applies a threshold function
to remove noise and uses contours to detect where
movement has occurred. Marks the area in which the movement
is and returns the center of the area as a point.
'''


def locate(delta):
    threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=0)
    cts, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    (x, y, w, h) = 0, 0, 0, 0

    for contour in cts:
        if cv2.contourArea(contour) < 300:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
    return x + w // 2, y + h // 2


'''
function that takes in a list of points and colors as well
as an image and draws lines between the points onto the image 
and returns the image.
'''


def draw(points, img):
    prev = None
    for coord in points:
        if coord[0] == -1 and coord[1] == -1:
            prev = None
            continue
        if prev is None:
            prev = coord
            continue
        cv2.line(img, (coord[0], coord[1]), (prev[0], prev[1]), coord[2], 5)
        prev = coord
    return img


class ColorSlider:

    def __init__(self):
        self.color = 0, 0, 0
        self.img = np.zeros((200, 200, 3), np.uint8)

    def read_red(self, x):
        b, g, r = self.color
        self.color = b, g, x
        self.img[:, :, 2] = x
        cv2.imshow("Color", self.img)

    def read_green(self, x):
        b, g, r = self.color
        self.color = b, x, r
        self.img[:, :, 1] = x
        cv2.imshow("Color", self.img)

    def read_blue(self, x):
        b, g, r = self.color
        self.color = x, g, r
        self.img[:, :, 0] = x
        cv2.imshow("Color", self.img)

    def set_color(self, color):
        b, g, r = color
        cv2.setTrackbarPos("Red", "Color", r)
        cv2.setTrackbarPos("Green", "Color", g)
        cv2.setTrackbarPos("Blue", "Color", b)
        self.read_red(r)
        self.read_blue(b)
        self.read_green(g)

    def create_sliders(self):
        cv2.namedWindow("Color")
        cv2.moveWindow("Color", 1282, 0)
        cv2.createTrackbar("Red", "Color", 0, 255, self.read_red)
        cv2.createTrackbar("Green", "Color", 255, 255, self.read_green)
        cv2.createTrackbar("Blue", "Color", 0, 255, self.read_blue)
        self.read_blue(0)
        self.read_red(0)
        self.read_green(255)

    def get_color(self):
        return self.color


def main():
    sliders = ColorSlider()
    showCamera(sliders)


if __name__ == '__main__':
    main()
