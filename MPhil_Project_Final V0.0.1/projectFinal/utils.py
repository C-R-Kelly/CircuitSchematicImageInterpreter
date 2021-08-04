# -*- coding: utf-8 -*-
"""
Image Processing
================

A set of functions for image processing

author: C. R. Kelly
email: CK598@cam.ac.uk

"""
from os.path import isfile, join, splitext
from os import listdir

from skimage.filters import threshold_otsu
from skimage.util import invert
from skimage.morphology import skeletonize

from PIL import Image, ImageOps

from .config import Config
config = Config()


def binaryConversion(image):
    """ Converts an image into a boolean binary Image.

    :param image: ndarray: Input image.
    :return: ndarray: Binary converted image.
    """
    binaryImage = image > threshold_otsu(image)
    binaryImage = invert(binaryImage)
    return binaryImage


def binarySkeleton(image):
    """ Converts an image into a boolean binarised skeletonised Image.

    :param image: ndarray: Input image.
    :return: ndarray: Binarised skeletonised image.
    """
    binaryImage = image > threshold_otsu(image)
    binaryImage = invert(binaryImage)
    binarySkeleton = skeletonize(binaryImage)
    return binarySkeleton


def addBorder(width=4, path=config.exportPath):
    """ Adds a border of white pixels around cropped component images to improve detection

    :param width: int: border size in every direction
    :param path: string: directory path were images are stored
    :return:
    """
    imageNames = [file for file in listdir(path) if
                  isfile(join(path, file)) and splitext(file)[1] == config.extension]
    for image in imageNames:
        inputImage = join(path, image)
        outputImage = join(path, image)
        ImageOps.expand(Image.open(inputImage), border=width, fill='white').save(outputImage)
        print(str(inputImage) + ' ----> ' + str(outputImage))

    return imageNames
