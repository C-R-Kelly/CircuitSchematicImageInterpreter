# -*- coding: utf-8 -*-
import os
import math
import random


from skimage.color import rgb2gray
from skimage.util import invert, img_as_int
from skimage.filters import threshold_otsu
from skimage.morphology import skeletonize

from scipy.ndimage import binary_fill_holes, rotate

from PIL import Image, ImageDraw, ImageFont

import numpy as np

# Output Page
PAGE = '0'
# Output DPI
DPI = (300, 300)
# Output Path
PATH = "/FINAL_MODEL_TESTING_DATA/MAX_CHAR\\"
# Canvas Height
canvasHeight = 75
# Image Number
IMAGE_NUMBER = 0


def drawCapacitor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height // 4  # calculate this function

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness
    if wireTails:
        canvasWidth = (2 * width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        tailLength = 0
        canvasWidth = (2 * width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)

    x1 = xc + width
    x2 = xc - width

    y1 = h
    y2 = h - (2 * height)

    yc = h - int((y1 - y2) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.line([(x1, y1), (x1, y2)], fill='BLACK', width=thickness)
    draw.line([(x2, y1), (x2, y2)], fill='BLACK', width=thickness)

    if wireTails:

        draw.line([(x1, yc), (x1 + tailLength, yc)], fill='BLACK', width=thickness)
        draw.line([(x2 - tailLength, yc), (x2, yc)], fill='BLACK', width=thickness)

        bbox = int(yc - height - 1), int(yc + height), int(xc - width - tailLength - 1), int(
            xc + width + tailLength)

    else:
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - 1), int(
            xc + width)

    # convert back to numpy array
    image = np.array(image)

    return image, bbox


def drawPotentiometer(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image[y1:y2, x1:x2] = 0

    # Hollow out to obtain desired line thickness
    y1, y2 = h - height + thickness, h - thickness,
    x1, x2 = int(xc - (width / 2)) + thickness, int(xc + (width / 2)) - thickness
    image[y1:y2, x1:x2] = 255

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Draw Arrows
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    radius = 4
    draw.regular_polygon(((xc, y1 - radius - thickness), radius), 3, 180, fill='BLACK')
    draw.line(((xc, y1 - radius - thickness), (xc, y1 - radius - thickness - 15)), width=thickness, fill='BLACK')

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)

    # convert back to numpy array
    image = np.array(image)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawUSPotentiometer(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

        # Draw zigzag line
        h, w = image.shape[0] - 15, image.shape[1]

        xc = int(w / 2)

        x1, x8 = int(xc - (width / 2)), int(xc + (width / 2))
        xint = math.ceil((x8 - x1) / 6)
        x2, x3, x4, x5, x6, x7 = x1 + (0.5 * xint), x1 + (1.5 * xint), x1 + (2.5 * xint), x1 + (3.5 * xint), x1 + (
                4.5 * xint), x1 + (5.5 * xint)

        y1, y2 = h - height, h
        yc = h - int((y2 - y1) / 2)

        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)

        draw.line([(x1, yc), (x2, y1)], fill='BLACK', width=thickness)
        draw.line([(x2, y1), (x3, y2)], fill='BLACK', width=thickness)
        draw.line([(x3, y2), (x4, y1)], fill='BLACK', width=thickness)
        draw.line([(x4, y1), (x5, y2)], fill='BLACK', width=thickness)
        draw.line([(x5, y2), (x6, y1)], fill='BLACK', width=thickness)
        draw.line([(x6, y1), (x7, y2)], fill='BLACK', width=thickness)
        draw.line([(x7, y2), (x8, yc)], fill='BLACK', width=thickness)

        image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Draw Arrows
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    radius = 4
    draw.regular_polygon(((xc, y1 - radius - thickness), radius), 3, 180, fill='BLACK')
    draw.line(((xc, y1 - radius - thickness), (xc, y1 - radius - thickness - 15)), width=thickness, fill='BLACK')

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    # convert back to numpy array
    image = np.array(image)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawResistor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image[y1:y2, x1:x2] = 0

    # Hollow out to obtain desired line thickness
    y1, y2 = h - height + thickness, h - thickness,
    x1, x2 = int(xc - (width / 2)) + thickness, int(xc + (width / 2)) - thickness
    image[y1:y2, x1:x2] = 255

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawLDR(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image[y1:y2, x1:x2] = 0

    # Hollow out to obtain desired line thickness
    y1, y2 = h - height + thickness, h - thickness,
    x1, x2 = int(xc - (width / 2)) + thickness, int(xc + (width / 2)) - thickness
    image[y1:y2, x1:x2] = 255

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Draw Arrows
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    gap = thickness / 2
    x1, x2, x3, x4 = xc - gap, xc + (width / 4) - gap, xc + (width / 4) + gap, xc + (width / 2) + gap
    y1, y2 = h - height - thickness - 5, h - height - (width / 6) - thickness - 5
    y3, y4 = h - height - thickness - 5, h - height - (width / 6) - thickness - 5

    if thickness >= 3:
        radius = 6
    elif thickness == 2:
        radius = 5
    else:
        radius = 3

    draw.regular_polygon((x1 - 1, y1 + 2, radius), 3, 260, fill='BLACK')
    draw.line(((x1, y1), (x2, y2)), width=thickness, fill='BLACK')

    draw.regular_polygon((x3 - 1, y3 + 2, radius), 3, 260, fill='BLACK')
    draw.line(((x3, y3), (x4, y4)), width=thickness, fill='BLACK')

    image = np.array(image)

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)

    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawThermistor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function for every component

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = width + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = width + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image[y1:y2, x1:x2] = 0

    # Hollow out to obtain desired line thickness
    y1, y2 = h - height + thickness, h - thickness,
    x1, x2 = int(xc - (width / 2)) + thickness, int(xc + (width / 2)) - thickness
    image[y1:y2, x1:x2] = 255

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # add thermistor lines
    length = height // 2
    image = Image.fromarray(image)
    y1, x1 = math.floor(yc - (height / 2) - 10), int(xc - (width / 2))
    y2, x2 = math.floor(yc - (height / 2) - 10), int(xc - (width / 2) + length)
    y3, x3 = math.floor(yc + (height / 2) + 5), int(xc + (width / 2))

    draw = ImageDraw.Draw(image)
    draw.line([(x1, y1), (x2, y2)], fill='BLACK', width=thickness)  # top line
    draw.line([(x2, y2), (x3, y3)], fill='BLACK', width=thickness)  # diagonal line

    image = np.array(image)

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawVarResistor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function for every component

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = width + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = width + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image[y1:y2, x1:x2] = 0

    # Hollow out to obtain desired line thickness
    y1, y2 = h - height + thickness, h - thickness,
    x1, x2 = int(xc - (width / 2)) + thickness, int(xc + (width / 2)) - thickness
    image[y1:y2, x1:x2] = 255

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # add thermistor lines
    length = height // 2
    image = Image.fromarray(image)
    y2, x2 = math.floor(yc - (height / 2) - 10), int(xc - (width / 2))
    y3, x3 = math.floor(yc + (height / 2) + 5), int(xc + (width / 2) - length)

    draw = ImageDraw.Draw(image)
    draw.line([(x2, y3), (x3, y2)], fill='BLACK', width=thickness)  # diagonal line
    radius = 6
    draw.regular_polygon(((x3, y2), radius), 3, 315, fill='BLACK')  # arrow head

    image = np.array(image)

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawUSVarResistor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function for every component

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = width + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = width + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

        # Draw zigzag line
        h, w = image.shape[0] - 15, image.shape[1]

        xc = int(w / 2)

        x1, x8 = int(xc - (width / 2)), int(xc + (width / 2))
        xint = math.ceil((x8 - x1) / 6)
        x2, x3, x4, x5, x6, x7 = x1 + (0.5 * xint), x1 + (1.5 * xint), x1 + (2.5 * xint), x1 + (3.5 * xint), x1 + (
                4.5 * xint), x1 + (5.5 * xint)

        y1, y2 = h - height, h
        yc = h - int((y2 - y1) / 2)

        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)

        draw.line([(x1, yc), (x2, y1)], fill='BLACK', width=thickness)
        draw.line([(x2, y1), (x3, y2)], fill='BLACK', width=thickness)
        draw.line([(x3, y2), (x4, y1)], fill='BLACK', width=thickness)
        draw.line([(x4, y1), (x5, y2)], fill='BLACK', width=thickness)
        draw.line([(x5, y2), (x6, y1)], fill='BLACK', width=thickness)
        draw.line([(x6, y1), (x7, y2)], fill='BLACK', width=thickness)
        draw.line([(x7, y2), (x8, yc)], fill='BLACK', width=thickness)

        image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # add arrow lines
    length = height // 2
    image = Image.fromarray(image)
    y2, x2 = math.floor(yc - (height / 2) - 10), int(xc - (width / 2))
    y3, x3 = math.floor(yc + (height / 2) + 5), int(xc + (width / 2) - length)

    draw = ImageDraw.Draw(image)
    draw.line([(x2, y3), (x3, y2)], fill='BLACK', width=thickness)  # diagonal line
    radius = 6
    draw.regular_polygon(((x3, y2), radius), 3, 310, fill='BLACK')  # arrow head

    image = np.array(image)

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawUSResistor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function
    extra = width % 6
    width = width - extra
    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw zigzag line
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)

    x1, x8 = int(xc - (width / 2)), int(xc + (width / 2))
    xint = math.ceil((x8 - x1) / 6)
    x2, x3, x4, x5, x6, x7 = x1 + (0.5 * xint), x1 + (1.5 * xint), x1 + (2.5 * xint), x1 + (3.5 * xint), x1 + (
                4.5 * xint), x1 + (5.5 * xint)

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.line([(x1, yc), (x2, y1)], fill='BLACK', width=thickness)
    draw.line([(x2, y1), (x3, y2)], fill='BLACK', width=thickness)
    draw.line([(x3, y2), (x4, y1)], fill='BLACK', width=thickness)
    draw.line([(x4, y1), (x5, y2)], fill='BLACK', width=thickness)
    draw.line([(x5, y2), (x6, y1)], fill='BLACK', width=thickness)
    draw.line([(x6, y1), (x7, y2)], fill='BLACK', width=thickness)
    draw.line([(x7, y2), (x8, yc)], fill='BLACK', width=thickness)

    image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawUSLDR(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw zigzag line
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x8 = int(xc - (width / 2)), int(xc + (width / 2))
    xint = math.ceil((x8 - x1) / 6)
    x2, x3, x4, x5, x6, x7 = x1 + (0.5 * xint), x1 + (1.5 * xint), x1 + (2.5 * xint), x1 + (3.5 * xint), x1 + (
            4.5 * xint), x1 + (5.5 * xint)

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.line([(x1, yc), (x2, y1)], fill='BLACK', width=thickness)
    draw.line([(x2, y1), (x3, y2)], fill='BLACK', width=thickness)
    draw.line([(x3, y2), (x4, y1)], fill='BLACK', width=thickness)
    draw.line([(x4, y1), (x5, y2)], fill='BLACK', width=thickness)
    draw.line([(x5, y2), (x6, y1)], fill='BLACK', width=thickness)
    draw.line([(x6, y1), (x7, y2)], fill='BLACK', width=thickness)
    draw.line([(x7, y2), (x8, yc)], fill='BLACK', width=thickness)

    image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Draw Arrows
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    gap = thickness / 2
    x1, x2, x3, x4 = xc - gap, xc + (width / 4) - gap, xc + (width / 4) + gap, xc + (width / 2) + gap
    y1, y2 = h - height - thickness - 5, h - height - (width / 6) - thickness - 5
    y3, y4 = h - height - thickness - 5, h - height - (width / 6) - thickness - 5

    if thickness >= 3:
        radius = 6
    elif thickness == 2:
        radius = 5
    else:
        radius = 3

    draw.regular_polygon((x1 - 1, y1 + 2, radius), 3, 260, fill='BLACK')
    draw.line(((x1, y1), (x2, y2)), width=thickness, fill='BLACK')

    draw.regular_polygon((x3 - 1, y3 + 2, radius), 3, 260, fill='BLACK')
    draw.line(((x3, y3), (x4, y4)), width=thickness, fill='BLACK')

    image = np.array(image)

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawUSThermistor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function for every component

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = width + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = width + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw zigzag line
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x8 = int(xc - (width / 2)), int(xc + (width / 2))
    xint = math.ceil((x8 - x1) / 6)
    x2, x3, x4, x5, x6, x7 = x1 + (0.5 * xint), x1 + (1.5 * xint), x1 + (2.5 * xint), x1 + (3.5 * xint), x1 + (
            4.5 * xint), x1 + (5.5 * xint)

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.line([(x1, yc), (x2, y1)], fill='BLACK', width=thickness)
    draw.line([(x2, y1), (x3, y2)], fill='BLACK', width=thickness)
    draw.line([(x3, y2), (x4, y1)], fill='BLACK', width=thickness)
    draw.line([(x4, y1), (x5, y2)], fill='BLACK', width=thickness)
    draw.line([(x5, y2), (x6, y1)], fill='BLACK', width=thickness)
    draw.line([(x6, y1), (x7, y2)], fill='BLACK', width=thickness)
    draw.line([(x7, y2), (x8, yc)], fill='BLACK', width=thickness)

    image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # add thermistor lines
    length = height // 2
    image = Image.fromarray(image)
    y1, x1 = math.floor(yc - (height / 2) - 5), int(xc - (width / 2))
    y2, x2 = math.floor(yc - (height / 2) - 5), int(xc - (width / 2) + length)
    y3, x3 = math.floor(yc + (height / 2) + 7), int(xc + (width / 2))

    draw = ImageDraw.Draw(image)
    draw.line([(x1, y1), (x2, y2)], fill='BLACK', width=thickness)  # top line
    draw.line([(x2, y2), (x7, y3)], fill='BLACK', width=thickness)  # diagonal line

    image = np.array(image)

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawDiode(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = int(height / 2)

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = (2 * width) + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (2 * width) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)

    x1 = xc + width
    x2 = xc - width

    y2 = h
    y3 = h - (2 * height)

    yc = h - int((y2 - y3) / 2)
    y1 = yc

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    if wireTails:

        draw.line([(x1, y1), (x1 + tailLength, y1)], fill='BLACK', width=thickness)
        draw.line([(x2 - tailLength, y1), (x2, y1)], fill='BLACK', width=thickness)

        # BBOX
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - tailLength - 1), int(
            xc + width + tailLength)

    else:
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - 1), int(
            xc + width)

    # draw top line
    draw.line([((x1 + 1), y2), ((x1 + 1), y3)], fill='BLACK', width=thickness)

    # draw bottom line
    draw.line([(x2, y2), (x2, y3)], fill='BLACK', width=thickness)

    # draw top diagonal
    for num in range(y3, yc):
        x2 += 1
        draw.line([(x2, y3), (x2, (y3 + thickness - 1))], fill='BLACK', width=thickness)
        y3 += 1

    # draw bottom diagonal
    x2 = xc - width
    for num in range(y2, yc, -1):
        x2 += 1
        draw.line([(x2, y2), (x2, (y2 - thickness + 1))], fill='BLACK', width=thickness)
        y2 -= 1

    # convert back to numpy array
    image = np.array(image)

    return image, bbox


def drawLED(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    if height > 25:
        height = 25
    width = int(height / 2)

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = (2 * width) + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (2 * width) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)

    x1 = xc + width
    x2 = xc - width

    y2 = h
    y3 = h - (2 * height)

    yc = h - int((y2 - y3) / 2)
    y1 = yc

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    if wireTails:

        draw.line([(x1, y1), (x1 + tailLength, y1)], fill='BLACK', width=thickness)
        draw.line([(x2 - tailLength, y1), (x2, y1)], fill='BLACK', width=thickness)

        # BBOX
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - tailLength - 1), int(
            xc + width + tailLength)

    else:
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - 1), int(
            xc + width)

    # draw top line
    draw.line([((x1 + 1), y2), ((x1 + 1), y3)], fill='BLACK', width=thickness)

    # draw bottom line
    draw.line([(x2, y2), (x2, y3)], fill='BLACK', width=thickness)

    # draw top diagonal
    for num in range(y3, yc):
        x2 += 1
        draw.line([(x2, y3), (x2, (y3 + thickness - 1))], fill='BLACK', width=thickness)
        y3 += 1

    # draw bottom diagonal
    x2 = xc - width
    for num in range(y2, yc, -1):
        x2 += 1
        draw.line([(x2, y2), (x2, (y2 - thickness + 1))], fill='BLACK', width=thickness)
        y2 -= 1

    # Draw Arrows
    x1, x2 = xc + (width / 2) - 1, xc + (width) - thickness + (border / 2) - 1
    y1, y2 = yc - height / 2 - 3, ((0 + yc - height) / 2) - 2

    x3, x4 = x1 - 7, x2 - 7
    y3, y4 = (yc - height / 2) - 9, ((0 + yc - height) / 2) - 4

    if thickness >= 3:
        radius = 4
    elif thickness == 2:
        radius = 3
    else:
        radius = 3

    draw.regular_polygon((x2 - 1, y2 + 2, radius), 3, 90, fill='BLACK')
    draw.line(((x1, y1), (x2, y2)), width=2, fill='BLACK')

    draw.regular_polygon((x4 - 2, y4 + 2, radius), 3, 90, fill='BLACK')
    draw.line(((x3, y3), (x4, y4)), width=2, fill='BLACK')

    # convert back to numpy array
    image = np.array(image)

    return image, bbox


def drawVoltmeter(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = (2 * width) + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (2 * width) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)

    x1 = xc + width
    x2 = xc - width

    y1 = h
    y2 = h - (2 * height)

    yc = h - int((y1 - y2) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.arc([(x2, y2), (x1, y1)], 0, 360, fill='BLACK', width=thickness)

    font = ImageFont.truetype('C:\\Windows\\Fonts\\Calibrib.ttf', size=height)
    draw.text((xc + 1, yc + (height / 4) - 2), text='V', anchor='mm', fill='BLACK', font=font, align='center')

    if wireTails:
        draw.line([(x1, yc), (x1 + tailLength, yc)], fill='BLACK', width=thickness)
        draw.line([(x2 - tailLength, yc), (x2, yc)], fill='BLACK', width=thickness)

        bbox = int(yc - height - 1), int(yc + height), int(xc - width - tailLength - 1), int(
            xc + width + tailLength)

    else:
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - 1), int(
            xc + width)

    # convert back to numpy array
    image = np.array(image)

    return image, bbox


def drawAmmeter(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = (2 * width) + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (2 * width) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)

    x1 = xc + width
    x2 = xc - width

    y1 = h
    y2 = h - (2 * height)

    yc = h - int((y1 - y2) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.arc([(x2, y2), (x1, y1)], 0, 360, fill='BLACK', width=thickness)

    font = ImageFont.truetype('C:\\Windows\\Fonts\\Calibrib.ttf', size=height)
    draw.text((xc + 1, yc + 1), text='A', anchor='mm', fill='BLACK', font=font, align='center')

    if wireTails:
        draw.line([(x1, yc), (x1 + tailLength, yc)], fill='BLACK', width=thickness)
        draw.line([(x2 - tailLength, yc), (x2, yc)], fill='BLACK', width=thickness)

        bbox = int(yc - height - 1), int(yc + height), int(xc - width - tailLength - 1), int(
            xc + width + tailLength)

    else:
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - 1), int(
            xc + width)

    # convert back to numpy array
    image = np.array(image)

    return image, bbox


def drawLightBulb(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = (2 * width) + (2 * tailLength) + border
        canvasImage = Image.new('RGB', (canvasWidth, canvasHeight))
        canvasImage = np.array(canvasImage)
        canvasImage[0:canvasImage.shape[0], 0:canvasImage.shape[1]] = 255
        canvasImage = Image.fromarray(canvasImage)
    else:
        canvasWidth = (2 * width) + border
        canvasImage = Image.new('RGB', (canvasWidth, canvasHeight))
        canvasImage = np.array(canvasImage)
        canvasImage[0:canvasImage.shape[0], 0:canvasImage.shape[1]] = 255
        canvasImage = Image.fromarray(canvasImage)
        tailLength = 0

    # Creating Light Bulb Canvas
    image = np.zeros(((2 * height) + 4, (2 * width) + 4, 3,), dtype=np.uint8)
    image[0:image.shape[0], 0:image.shape[1]] = 255

    # Calculating drawing variables
    h, w = image.shape[0], image.shape[1]

    xc = int(w / 2)
    x1 = xc + width
    x2 = xc - width

    yc = int(h / 2)
    y1 = yc + height
    y2 = yc - height

    # Converting to PIL
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # Drawing Light Bulb
    draw.line([(x1, yc), (x2, yc)], fill='BLACK', width=thickness)
    draw.line([(xc, y1), (xc, y2)], fill='BLACK', width=thickness)
    draw.arc([(x2, y2), (x1, y1)], 0, 360, fill='BLACK', width=thickness)

    # Converting to NUMPY & Rotating to give correct rotation
    image = np.array(image)
    image = rotate(image, 45, reshape=False, cval=255, output=np.uint8)

    # Converting back to PIL
    image = Image.fromarray(image)  # lightbulb symbol

    # Pasting lightbulb onto blank canvas
    canvasImage.paste(image, ((canvasWidth // 2) - width - 2, canvasHeight - (2 * height) - 15))

    draw = ImageDraw.Draw(canvasImage)

    if wireTails:
        # drawing wire tails
        yc = canvasHeight - 15 - (height) + 1

        x1 = 0 + border - thickness - 3
        x2 = x1 + tailLength
        x3 = x2 + width + width
        x4 = x3 + tailLength

        draw.line([(x1, yc), (x2, yc)], fill='BLACK', width=thickness)
        draw.line([(x3, yc), (x4, yc)], fill='BLACK', width=thickness)

        bbox = int(yc - height - 1), int(yc + height), int(xc - width - tailLength - 1), int(
            xc + width + tailLength)

    else:
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - 1), int(
            xc + width)

    # convert back to numpy array
    canvasImage = np.array(canvasImage)
    image = np.array(image)

    return canvasImage, image


def drawMotor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    # Draw Blank Canvas
    if wireTails:
        canvasWidth = (2 * width) + (2 * tailLength) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (2 * width) + border

        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)

    x1 = xc + width
    x2 = xc - width

    y1 = h
    y2 = h - (2 * height)

    yc = h - int((y1 - y2) / 2)
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.arc([(x2, y2), (x1, y1)], 0, 360, fill='BLACK', width=thickness)

    font = ImageFont.truetype('C:\\Windows\\Fonts\\Calibrib.ttf', size=height)
    draw.text((xc + 1, yc + (height / 4) - 2), text='M', anchor='mm', fill='BLACK', font=font, align='center')

    if wireTails:
        draw.line([(x1, yc), (x1 + tailLength, yc)], fill='BLACK', width=thickness)
        draw.line([(x2 - tailLength, yc), (x2, yc)], fill='BLACK', width=thickness)

        bbox = int(yc - height - 1), int(yc + height), int(xc - width - tailLength - 1), int(
            xc + width + tailLength)

    else:
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - 1), int(
            xc + width)

    # convert back to numpy array
    image = np.array(image)

    return image, bbox


def drawCell(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height // 4  # calculate this function

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness
    if wireTails:
        canvasWidth = (2 * width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        tailLength = 0
        canvasWidth = (2 * width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)

    x1 = xc - width
    x2 = xc + width

    y1 = h
    y2 = h - (2 * height)

    gap = 0.25 * (y1 - y2)
    y3 = y1 - gap
    y4 = y2 + gap

    yc = h - int((y1 - y2) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.line([(x1, y1), (x1, y2)], fill='BLACK', width=thickness)
    draw.line([(x2, y3), (x2, y4)], fill='BLACK', width=thickness)

    if wireTails:

        draw.line([(x1, yc), (x1 + tailLength, yc)], fill='BLACK', width=thickness)
        draw.line([(x2 - tailLength, yc), (x2, yc)], fill='BLACK', width=thickness)

        bbox = int(yc - height - 1), int(yc + height), int(xc - width - tailLength - 1), int(
            xc + width + tailLength)

    else:
        bbox = int(yc - height - 1), int(yc + height), int(xc - width - 1), int(
            xc + width)

    # convert back to numpy array
    image = np.array(image)

    return image, bbox


def drawOpenSwitch(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 2  # calculate this function
    if width < 48:
        width = 48

    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = width + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = width + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # starting circle
    offset = 7
    start1 = x1, yc - offset
    finish1 = x1 + 2 * offset, yc + offset
    draw.arc([start1, finish1], 0, 360, fill='BLACK', width=thickness)

    # ending circle
    start2 = x2 - 2 * offset, yc - offset
    finish2 = x2, yc + offset
    draw.arc([start2, finish2], 0, 360, fill='BLACK', width=thickness)

    # switching wire
    draw.line([(x1 + 2 * offset, yc), (finish2[0] - 2 * offset, y1)], fill='BLACK', width=thickness)
    image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawClosedSwitch(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 2  # calculate this function
    if width < 48:
        width = 48
    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = width + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = width + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # starting circle
    offset = 7
    start1 = x1, yc - offset
    finish1 = x1 + 2 * offset, yc + offset
    draw.arc([start1, finish1], 0, 360, fill='BLACK', width=thickness)

    # ending circle
    start2 = x2 - 2 * offset, yc - offset
    finish2 = x2, yc + offset
    draw.arc([start2, finish2], 0, 360, fill='BLACK', width=thickness)

    # switching wire
    draw.line([(x1 + 2 * offset, yc), (finish2[0] - 2 * offset, yc)], fill='BLACK', width=thickness)
    image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawRelay1(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 2  # calculate this function
    if width < 48:
        width = 48
    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = width + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = width + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # starting circle
    offset = 7
    start1 = x1, yc - offset
    finish1 = x1 + 2 * offset, yc + offset
    draw.arc([start1, finish1], 0, 360, fill='BLACK', width=thickness)

    # ending circle upper
    start2 = x2 - 2 * offset, y1 - offset
    finish2 = x2, y1 + offset
    draw.arc([start2, finish2], 0, 360, fill='BLACK', width=thickness)

    # ending circle lower
    start2 = x2 - 2 * offset, y2 - offset
    finish2 = x2, y2 + offset
    draw.arc([start2, finish2], 0, 360, fill='BLACK', width=thickness)

    # switching wire
    draw.line([(x1 + 2 * offset, yc), (finish2[0] - 2 * offset, y1)], fill='BLACK', width=thickness)
    image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawRelay2(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 2  # calculate this function
    if width < 48:
        width = 48
    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = width + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = width + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw filled rectangle
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # starting circle
    offset = 7
    start1 = x1, yc - offset
    finish1 = x1 + 2 * offset, yc + offset
    draw.arc([start1, finish1], 0, 360, fill='BLACK', width=thickness)

    # ending circle upper
    start2 = x2 - 2 * offset, y1 - offset
    finish2 = x2, y1 + offset
    draw.arc([start2, finish2], 0, 360, fill='BLACK', width=thickness)

    # ending circle lower
    start2 = x2 - 2 * offset, y2 - offset
    finish2 = x2, y2 + offset
    draw.arc([start2, finish2], 0, 360, fill='BLACK', width=thickness)

    # switching wire
    draw.line([(x1 + 2 * offset, yc), (finish2[0] - 2 * offset, y2)], fill='BLACK', width=thickness)
    image = np.array(image)

    if wireTails:

        # Add 'wire' tails

        if thickness == 1:

            y1, x1, = yc, xc - (int(width / 2)) - tailLength
            y2, x2, = yc + 1, xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc, xc + (int(width / 2))
            y2, x2, = yc + 1, xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0

        else:

            y1, x1, = yc - (int(thickness / 2)), xc - (int(width / 2)) - tailLength
            y2, x2, = yc + (int(thickness / 2)), xc - (int(width / 2))
            image[y1:y2, x1:x2] = 0

            y1, x1, = yc - (int(thickness / 2)), xc + (int(width / 2))
            y2, x2, = yc + (int(thickness / 2)), xc + (int(width / 2)) + tailLength
            image[y1:y2, x1:x2] = 0
    else:
        tailLength = 0

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawInductor(height, thickness, tailLength, wireTails=False, Filled=False, Skel=False):
    width = height * 3  # calculate this function
    extra = width % 3
    width = width - extra
    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Draw arcs line
    h, w = image.shape[0] - 15, image.shape[1]

    xc = int(w / 2)
    x1, x5 = int(xc - (width / 2)), int(xc + (width / 2))
    xint = math.ceil((x5 - x1) / 4)
    x2, x3, x4, = x1 + xint, x1 + (2 * xint), x1 + (3 * xint)

    y1, y2 = h - height + 10, h + 10
    yc = h - int((y2 - y1) / 2)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    draw.arc([(x1, y1), (x2, y2)], 180, 360, fill='BLACK', width=thickness)
    draw.arc([(x2, y1), (x3, y2)], 180, 360, fill='BLACK', width=thickness)
    draw.arc([(x3, y1), (x4, y2)], 180, 360, fill='BLACK', width=thickness)
    draw.arc([(x4, y1), (x5, y2)], 180, 360, fill='BLACK', width=thickness)

    if wireTails:

        # Add 'wire' tails
        if thickness == 1:
            ypoint = math.ceil((y2 - y1) / 2)
            draw.line([(x1 - tailLength, y1 + ypoint), (x1, y1 + ypoint)], fill='BLACK', width=thickness)
            draw.line([(x5, y1 + ypoint), (x5 + tailLength, y1 + ypoint)], fill='BLACK', width=thickness)
            print(y1, y2)
        elif thickness == 2:
            ypoint = math.ceil((y2 - y1) / 2)
            draw.line([(x1 - tailLength, y1 + ypoint - thickness), (x1, y1 + ypoint - thickness)], fill='BLACK',
                      width=thickness)
            draw.line([(x5, y1 + ypoint - thickness), (x5 + tailLength, y1 + ypoint - thickness)], fill='BLACK',
                      width=thickness)
            print(y1, y2)
        elif thickness == 3:
            ypoint = math.ceil((y2 - y1) / 2)
            draw.line([(x1 - tailLength, y1 + ypoint - thickness + 1), (x1, y1 + ypoint - thickness + 1)], fill='BLACK',
                      width=thickness)
            draw.line([(x5, y1 + ypoint - thickness + 1), (x5 + tailLength, y1 + ypoint - thickness + 1)], fill='BLACK',
                      width=thickness)
            print(y1, y2)
        elif thickness == 4:
            ypoint = math.ceil((y2 - y1) / 2)
            draw.line([(x1 - tailLength, y1 + ypoint - thickness + 1), (x1, y1 + ypoint - thickness + 1)], fill='BLACK',
                      width=thickness)
            draw.line([(x5, y1 + ypoint - thickness + 1), (x5 + tailLength, y1 + ypoint - thickness + 1)], fill='BLACK',
                      width=thickness)
        elif thickness == 5:
            ypoint = math.ceil((y2 - y1) / 2)
            draw.line([(x1 - tailLength, y1 + ypoint - thickness + 2), (x1, y1 + ypoint - thickness + 2)], fill='BLACK',
                      width=thickness)
            draw.line([(x5, y1 + ypoint - thickness + 2), (x5 + tailLength, y1 + ypoint - thickness + 2)], fill='BLACK',
                      width=thickness)

    else:
        tailLength = 0

    # convert back to numpy array
    image = np.array(image)

    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawNPNTransistor(height, thickness, tailLength=13, wireTails=True, Filled=False, Skel=False):
    width = height * 2  # calculate this function
    height = height * 2
    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness
    if thickness > 3:
        thickness = 3

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Drawing
    h, w = image.shape[0] - 10, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    # PIL Conversion
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # Draw Cricle
    draw.arc([(x1, y1), (x2, y2)], 0, 360, fill='BLACK', width=thickness)

    # draw inside lines
    # left vert line
    offset = height / 5
    draw.line([(xc - offset, yc - offset), (xc - offset, yc + offset)], fill='BLACK', width=thickness)
    # left horiz line
    draw.line([(x1 - 5, yc), (xc - offset, yc)], fill='BLACK', width=thickness)

    # right vert lines
    draw.line([(xc + offset, y1 - 3), (xc + offset, yc - offset)], fill='BLACK', width=thickness)  # top
    draw.line([(xc + offset, yc + offset), (xc + offset, y2 + 3)], fill='BLACK', width=thickness)  # bottom

    # draw  diagonal lines
    draw.line([(xc - offset, yc - 2), (xc + offset, yc - offset - 1)], fill='BLACK', width=thickness)  # top
    draw.line([(xc - offset, yc + 2), (xc + offset, yc + offset + 1)], fill='BLACK', width=thickness)  # bottom

    # draw arrowhead
    draw.regular_polygon(((xc + 2, yc - (height / 8) - 1), 5), n_sides=3, fill='BLACK', rotation=0)
    image = np.array(image)
    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose # th


def drawPNPTransistor(height, thickness, tailLength=13, wireTails=True, Filled=False, Skel=False):
    width = height * 2  # calculate this function
    height = height * 2
    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness
    if thickness > 3:
        thickness = 3

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Drawing
    h, w = image.shape[0] - 10, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    # PIL Conversion
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # Draw Cricle
    draw.arc([(x1, y1), (x2, y2)], 0, 360, fill='BLACK', width=thickness)

    # draw inside lines
    # left vert line
    offset = height / 5
    draw.line([(xc - offset, yc - offset), (xc - offset, yc + offset)], fill='BLACK', width=thickness)
    # left horiz line
    draw.line([(x1 - 5, yc), (xc - offset, yc)], fill='BLACK', width=thickness)

    # right vert lines
    draw.line([(xc + offset, y1 - 3), (xc + offset, yc - offset)], fill='BLACK', width=thickness)  # top
    draw.line([(xc + offset, yc + offset), (xc + offset, y2 + 3)], fill='BLACK', width=thickness)  # bottom

    # draw  diagonal lines
    draw.line([(xc - offset, yc - 2), (xc + offset, yc - offset - 1)], fill='BLACK', width=thickness)  # top
    draw.line([(xc - offset, yc + 2), (xc + offset, yc + offset + 1)], fill='BLACK', width=thickness)  # bottom

    # draw arrowhead
    draw.regular_polygon(((xc, yc + (height / 8) + 1), 5), n_sides=3, fill='BLACK', rotation=115)
    image = np.array(image)
    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def drawMOSFET(height, thickness, tailLength=13, wireTails=False, Filled=False, Skel=False):
    width = height * 2  # calculate this function
    height = height * 2
    if thickness == 1:
        border = 9
    else:
        border = 9 + thickness
    if thickness > 3:
        thickness = 3

    if wireTails:
        canvasWidth = (width) + (2 * tailLength) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255
    else:
        canvasWidth = (width) + border
        # draw blank canvas:
        image = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)
        image[0:image.shape[0], 0:image.shape[1]] = 255

    # Drawing
    h, w = image.shape[0] - 10, image.shape[1]

    xc = int(w / 2)
    x1, x2 = int(xc - (width / 2)), int(xc + (width / 2))

    y1, y2 = h - height, h
    yc = h - int((y2 - y1) / 2)

    # PIL Conversion
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # Draw Cricle
    # draw.arc([(x1, y1), (x2, y2)], 0, 360, fill='BLACK', width=thickness)

    # draw inside lines
    # left vert line
    offset = height / 10
    draw.line([(xc - offset, y1), (xc - offset, y2 + 3)], fill='BLACK', width=thickness)
    # left horiz line
    draw.line([(x1, yc + 2), (xc - offset, yc + 2)], fill='BLACK', width=thickness)

    # right vert lines
    draw.line([(xc + offset, y1), (xc + offset, yc - 8)], fill='BLACK', width=thickness)  # top
    draw.line([(xc + offset, yc - 5), (xc + offset, yc + 10)], fill='BLACK', width=thickness)  # middle
    draw.line([(xc + offset, yc + 13), (xc + offset, y2 + 3)], fill='BLACK', width=thickness)  # bottom
    draw.line([(x2, y1 - 2), (x2, ((yc + y1 - 14) / 2) + 2)], fill='BLACK', width=thickness)  # far right top
    draw.line([(x2, yc + 2), (x2, y2 + 3)], fill='BLACK', width=thickness)  # far right bottom

    # draw  right horiz lines
    draw.line([(xc + offset, ((yc + y1 - 14) / 2) + 2), (x2, ((yc + y1 - 14) / 2) + 2)], fill='BLACK',
              width=thickness)  # top
    draw.line([(xc + offset, yc + 2), (x2, yc + 2)], fill='BLACK', width=thickness)  # middle
    draw.line([(xc + offset, (yc + y2 + 16) / 2), (x2, (yc + y2 + 16) / 2)], fill='BLACK', width=thickness)  # bottom

    # draw arrowhead
    radius = 5
    xtri, ytri = xc + offset + radius, yc + 2
    draw.regular_polygon(((xtri, ytri), radius), n_sides=3, fill='BLACK', rotation=90)
    image = np.array(image)
    # Calculate bounding box of finished resistor
    bboxTight = int(yc - (height / 2)), int(yc + (height / 2) - 1), int(
        xc - (width / 2) - tailLength), int(xc + (width / 2) + tailLength - 1)
    bboxLoose = int(yc - (height / 2) - 1), int(yc + (height / 2)), int(
        xc - (width / 2) - tailLength - 1), int(xc + (width / 2) + tailLength)
    return image, bboxLoose  # Can choose which bounding box to add to box file by changing to bboxTight/bboxLoose


def skeletonization(image):
    image = rgb2gray(image)  # converts to gray scale
    threshold = threshold_otsu(image)  # creates a threshold (above is 'on' below is off'
    binaryImage = image > threshold  # applies threshold to image
    binaryImage = invert(
        binaryImage)  # inverts image (skelentonize works on a image with a black background with white pixels)
    image = skeletonize(binaryImage)  # skeletonizes image
    image = invert(image)  # inverts again to bring back white background with black pixels for component
    image = img_as_int(image)  # converts image to int data type
    return image


def thresholdImage(image):
    image = rgb2gray(image)  # converts to gray scale
    threshold = threshold_otsu(image)  # creates a threshold (above is 'on' below is off'
    binaryImage = image > threshold  # applies threshold to image
    binaryImage = invert(binaryImage)
    image = binary_fill_holes(binaryImage)
    image = invert(image)
    image = img_as_int(image)  # converts image to ubyte data type
    return image


def generateTextLine(ImageNumber, Filled=False, Skel=False):
    Images = []
    # Canvas Width Var Holder
    canvasWidth = 0
    # Assign Character Length
    charLength = random.randrange(5, 30, 1)
    # Assign Character Height
    charHeight = random.randrange(16, 30, 2)
    # Assign Line Thickness
    lineThickness = random.randrange(1, 5, 1)

    LastCharacterSpace = False

    # Open GT File
    GT_PATH = os.path.join(PATH, "image" + str(ImageNumber) + ".gt.txt")
    gtFile = open(GT_PATH, mode='w', encoding='utf-8')
    # Retrieve images
    for characterLength in range(0, charLength):

        # Decide if a space is going to be included

        isSpaces = random.randrange(1, 15, 1)  # 15 for no spaces, 16 for spaces

        if isSpaces == 15 and not LastCharacterSpace:
            image = Image.new('RGB', (canvasHeight // 2, canvasHeight))
            image = np.array(image)
            image[0:image.shape[0], 0:image.shape[1]] = 255
            LastCharacterSpace = True
            gtFile.write(' ')
            component = 'SPACE'

        else:

            if Filled:
                # Assign character to create
                char = random.randrange(0, 7, 1)
                if char == 0:
                    component = 'RESISTOR'
                    image, bbox = drawResistor(charHeight, lineThickness, 10, wireTails=True)
                    gtFile.write('1')
                    image = thresholdImage(image)
                    Images.append(image)
                    print(component, "| Filled")
                elif char == 1:
                    component = 'THERMISTOR'
                    image, bbox = drawThermistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('2')
                    image = thresholdImage(image)
                    Images.append(image)
                    print(component, "| Filled")
                elif char == 2:
                    component = 'DIODE'
                    image, bbox = drawDiode(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('3')
                    image = thresholdImage(image)
                    Images.append(image)
                    print(component, "| Filled")
                elif char == 3:
                    component = 'LDR'
                    image, bbox = drawLDR(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('8')
                    image = thresholdImage(image)
                    Images.append(image)
                    print(component, "| Filled")
                elif char == 4:
                    component = 'LED'
                    image, bbox = drawLED(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('9')
                    image = thresholdImage(image)
                    Images.append(image)
                    print(component, "| Filled")
                elif char == 5:
                    component = 'POTENTIOMETER'
                    image, bbox = drawPotentiometer(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('[')
                    image = thresholdImage(image)
                    Images.append(image)
                    print(component, "| Filled")
                elif char == 6:
                    component = 'VARIABLE RESISTOR'
                    image, bbox = drawVarResistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write(']')
                    image = thresholdImage(image)
                    Images.append(image)
                    print(component, "| Filled")

                LastCharacterSpace = False


            else:

                # Assign character to create
                char = random.randrange(0, 26, 1)

                if char == 0:
                    component = 'CAPACITOR'
                    image, bbox = drawCapacitor(charHeight, lineThickness, 10, wireTails=True)
                    gtFile.write('0')
                elif char == 1:
                    component = 'RESISTOR'
                    image, bbox = drawResistor(charHeight, lineThickness, 10, wireTails=True)
                    gtFile.write('1')
                elif char == 2:
                    component = 'THERMISTOR'
                    image, bbox = drawThermistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('2')
                elif char == 3:
                    component = 'DIODE'
                    image, bbox = drawDiode(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('3')
                elif char == 4:
                    component = 'VOLTMETER'
                    image, bbox = drawVoltmeter(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('4')
                elif char == 5:
                    component = 'AMMETER'
                    image, bbox = drawAmmeter(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('5')
                elif char == 6:
                    component = 'LIGHTBULB'
                    image, bbox = drawLightBulb(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('6')
                elif char == 7:
                    component = 'MOTOR'
                    image, bbox = drawMotor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('7')
                elif char == 8:
                    component = 'LDR'
                    image, bbox = drawLDR(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('8')
                elif char == 9:
                    component = 'LED'
                    image, bbox = drawLED(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('9')
                elif char == 10:
                    component = 'CELL'
                    image, bbox = drawCell(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('@')
                elif char == 11:
                    component = 'POTENTIOMETER'
                    image, bbox = drawPotentiometer(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('[')
                elif char == 12:
                    component = 'VARIABLE RESISTOR'
                    image, bbox = drawVarResistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write(']')
                elif char == 13:
                    component = 'US RESISTOR'
                    image, bbox = drawUSResistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('+')
                elif char == 14:
                    component = 'US THERMISTOR'
                    image, bbox = drawUSThermistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('-')
                elif char == 15:
                    component = 'US LDR'
                    image, bbox = drawUSLDR(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('*')
                elif char == 16:
                    component = 'US POTENTIOMETER'
                    image, bbox = drawUSPotentiometer(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('{')
                elif char == 17:
                    component = 'US VARIABLE RESISTOR'
                    image, bbox = drawUSVarResistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('}')
                elif char == 18:
                    component = 'OPEN SWITCH'
                    image, bbox = drawOpenSwitch(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('<')
                elif char == 19:
                    component = 'CLOSED SWITCH'
                    image, bbox = drawClosedSwitch(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('>')
                elif char == 20:
                    component = 'RELAY 1'
                    image, bbox = drawRelay1(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('\\')
                elif char == 21:
                    component = 'RELAY 2'
                    image, bbox = drawRelay2(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('/')
                elif char == 22:
                    component = 'NPN TRANSISTOR'
                    image, bbox = drawNPNTransistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('A')
                elif char == 23:
                    component = 'PNP TRANSISTOR'
                    image, bbox = drawPNPTransistor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('a')
                elif char == 24:
                    component = 'MOSFET'
                    image, bbox = drawMOSFET(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write('(')
                elif char == 25:
                    component = 'INDUCTOR'
                    image, bbox = drawInductor(charHeight, lineThickness, 15, wireTails=False)
                    gtFile.write(')')

                LastCharacterSpace = False

                # Perform any extra operations & add image to canvas
                if Skel and not Filled and not component == 'SPACE':
                    image = skeletonization(image)
                    Images.append(image)
                    print(component, "| Skeletonized")

                elif Filled and not component == 'SPACE':
                    Images.append(image)
                    print(component, "| Filled")
                elif component == 'SPACE':
                    Images.append(image)
                    print()
                else:
                    Images.append(image)
                    print(component)

    gtFile.close()

    # Retrieve Canvas Width
    for imWidth in Images:
        canvasWidth += imWidth.shape[1]

    # Pasting Images Onto Canvas
    FULL_IMAGE = Image.new('L', (canvasWidth, canvasHeight))
    widthCounter = 0
    for image in Images:
        image = Image.fromarray(image)
        FULL_IMAGE.paste(image, (widthCounter, 0))
        widthCounter += image.width

    # Saving Image To File
    width, height = int(FULL_IMAGE.width * 0.6), int(FULL_IMAGE.height * 0.6)
    FULL_IMAGE = FULL_IMAGE.resize((width, height))
    FULL_IMAGE_PATH = os.path.join(PATH, "image" + str(ImageNumber) + ".tif")
    FULL_IMAGE.save(FULL_IMAGE_PATH)
    FULL_IMAGE = np.array(FULL_IMAGE)

    return FULL_IMAGE, charLength


def main(NoOfImages, Filled=False, Skel=False, Random=False):
    for imageNo in range(0, NoOfImages):
        if Random:
            number = random.randrange(0, 10000000, 1)
            IMAGE_PATH = os.path.join(PATH, "image" + str(number) + ".tif")
            fileExists = os.path.isfile(IMAGE_PATH)
            while fileExists:
                number = random.randrange(0, 10000000, 1)
                IMAGE_PATH = os.path.join(PATH, "image" + str(number) + ".tif")
                fileExists = os.path.isfile(IMAGE_PATH)
        else:
            number = imageNo

        image, size = generateTextLine(number, Filled=Filled, Skel=Skel)
        print("Image: " + PATH + "image" + str(number) + ".tif Generated | Size: " + str(size))
        print()
        print()
    return


#main(500, Filled=False, Skel=False, Random=True)
#main(500, Filled=True, Skel=False, Random=True)
#main(500, Filled=False, Skel=True, Random=True)


#main(2600, Filled=False, Skel=True, Random=False)