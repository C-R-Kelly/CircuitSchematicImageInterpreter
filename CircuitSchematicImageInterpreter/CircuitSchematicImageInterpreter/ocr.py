# -*- coding: utf-8 -*-
"""
Tesseract OCR
=============

Using OCR to identify segmented components

author: C. R. Kelly
email: CK598@cam.ac.uk

"""
import numpy as np

import matplotlib.pyplot as plt

from skimage.io import imread
from scipy.ndimage import rotate

from os import path

from PIL import Image, ImageOps

import pytesseract as pyt

from .config import Config
from .component_map import getComponents

config = Config()

LANG_MODEL = config.langModel
CONFIG = config.configLine

# Initialising Tesseract
pyt.pytesseract.tesseract_cmd = config.TessPath


def OCR(OCR_Result):
    """ Matches OCR result to corresponding component

    :param OCR_Result: str: Single character returned by tesseract
    :return list: Identified component, unichar and no. of terminals
    """
    Component_List = getComponents()
    for i in range(len(Component_List)):
        if Component_List[i][1] == str(OCR_Result):
            foundComponent = Component_List[i]
            return foundComponent
    return 'NULL FOUND - CHECK DATA', 'NULL', 0


def OCRComponents(components, Display=config.display):
    """ Compiles & rotates all found components into a single horizontal image and applies Tesseract OCR

    :param Display: boolean: display graphical OCR results
    :param components: list: List of found component classes
    :return nil:
    """
    # Retrieve Canvas Width & Height
    canvasHeight = config.componentWidth + 15
    canvasWidth = 0
    for component in components:
        if component.isVert:
            canvasWidth += component.Height + 10

        else:
            canvasWidth += component.Width + 10
    canvasWidth += 20

    # Pasting Images Onto Canvas
    FULL_IMAGE = Image.new('L', (canvasWidth, canvasHeight), color=255)
    widthCounter = 10
    for component in components:
        componentImage = imread(component.path)

        if component.isVert:
            componentImage = rotate(componentImage, 90, reshape=True, cval=255, output=np.uint8)
        componentImagePIL = Image.fromarray(componentImage)
        componentImagePIL = ImageOps.expand(componentImagePIL, border=10, fill='white')
        FULL_IMAGE.paste(componentImagePIL, (widthCounter, 0))
        widthCounter += componentImage.shape[1] + 10

    # Saving full image
    FULL_IMAGE_PATH = path.join(config.exportPath, 'ALL_COMPONENTS' + config.extension)
    FULL_IMAGE.save(FULL_IMAGE_PATH)
    FULL_IMAGE = np.array(FULL_IMAGE)

    # Performing Tesseract OCR
    OCR_Result = pyt.image_to_string(FULL_IMAGE, lang=LANG_MODEL, config=CONFIG)
    OCR_Result = OCR_Result.split('\n')
    OCR_Result = list(OCR_Result[0])

    if Display:
        foundTextAsBoxes_1 = pyt.image_to_boxes(FULL_IMAGE, lang=LANG_MODEL, config=CONFIG)
        foundTextAsBoxes_1 = foundTextAsBoxes_1.splitlines()
        #### FIGURE GENERATION
        # Generating figure
        if not len(plt.get_fignums()) == 0:
            figs = plt.get_fignums()
            plt.figure(len(figs) + 1)
        fig, ax = plt.subplots()

        ax.set_xlim((0, FULL_IMAGE.shape[1]))
        ax.set_ylim((FULL_IMAGE.shape[0], 0))
        # ax.set_title('Model: ' + LANG_MODEL + ' | Image: OCR_Boxes.png' + ' | OCR RESULT')
        ax.imshow(FULL_IMAGE, cmap=plt.cm.gray)

        # plotting box
        for boxes in foundTextAsBoxes_1:
            bboxData = boxes.split(' ')
            # bboxData = foundTextAsBoxes_1[1].split(' ')
            char = bboxData[0]
            bbox = FULL_IMAGE.shape[0] - int(bboxData[4]), FULL_IMAGE.shape[0] - int(bboxData[2]), int(
                bboxData[1]), int(
                bboxData[3])

            top, bottom, left, right = bbox
            ax.plot((left, right), (top, top), c='r')
            ax.plot((left, right), (bottom, bottom), c='r')
            ax.plot((left, left), (top, bottom), c='r')
            ax.plot((right, right), (top, bottom), c='r')
            ax.text(left + int((right - left) / 2), (top - 2), char)

        plt.show()
        plt.savefig(path.join(config.exportPath, 'OCR_Boxes.png'))

    # Identifying each component, its unichar and No. of terminals
    for i in range(len(OCR_Result)):
        foundComponent = OCR(OCR_Result[i])
        if i < len(components):
            components[i].componentType = foundComponent[0]
            components[i].unichar = foundComponent[1]
            # components[i].terminalNo = foundComponent[2]
            components[i].terminalNo = 2
