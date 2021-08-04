# -*- coding: utf-8 -*-
########  CONFIG  ########

LANG_MODEL1 = 'model_project_final'
TITLE_ONE = LANG_MODEL1
CONFIG1 = '--psm 13 --dpi 300 -c tessedit_char_whitelist=0123456789@[]+-*{}<>/Aa()\\\ -c load_system_dawg=false -c load_freq_dawg=false'

TESTING_DATA = '' # Path to testing data or directories with testing data in.

TEST_DIR = False # If true, each of the entries in "TESTING_DIRS" list will be tested separately. If false, script assumes all testing data is at the location "TESTING_DATA".
TESTING_DIRS = 'NORMAL', 'FILLED', 'SKEL'

##########################

import os
from os import listdir
from os.path import isfile, join, splitext

from skimage import io, img_as_ubyte

import matplotlib.pyplot as plt

import pytesseract as pyt


# Image importation handling
def importImage(path):
    """ Imports a given image and converts it into two copies, one as grayscale, one as a binarized skeletonized copy.

    :param path: str: File path of the image.
    :return image: ndarray: Grayscale conversion of imported image.
    :return binaryImage: ndarray: Binarized Skeletonized copy of imported image.
    """

    image = io.imread(path)
    if len(image.shape) == 2:

        image = img_as_ubyte(image)
        return image
    else:
        image = image[:, :, 0]
        image = img_as_ubyte(image)
        return image


# Obtain all file names in the image directory
def getFileNames(directory_path):
    fileNames = [file for file in listdir(directory_path) if
                 isfile(join(directory_path, file)) and splitext(file)[1] == '.tif']
    GTFiles = [file for file in listdir(directory_path) if
               isfile(join(directory_path, file)) and splitext(file)[1] == '.txt']
    return fileNames, GTFiles


# Read ground truth from .gt.txt file
def getGroundTruth(gt_file_path):
    gt_file = open(gt_file_path, 'r')
    groundTruth = gt_file.readline()
    gt_file.close()
    return groundTruth


# Display graphical results
def showGraphics(file):
    image = importImage(os.path.join(TESTING_DATA, file))
    foundTextAsString_1 = pyt.image_to_string(image, lang=LANG_MODEL1, config=CONFIG1)
    foundTextAsString_1 = foundTextAsString_1.split('\n')
    foundTextAsBoxes_1 = pyt.image_to_boxes(image, lang=LANG_MODEL1, config=CONFIG1)
    foundTextAsBoxes_1 = foundTextAsBoxes_1.splitlines()

    #### FIGURE GENERATION
    # Generating figure
    fig, ax = plt.subplots()

    ax.set_xlim((0, image.shape[1]))
    ax.set_ylim((image.shape[0], 0))
    ax.set_title('Model: ' + LANG_MODEL1 + ' | Image: ' + file + ' | OCR RESULT')
    ax.imshow(image, cmap=plt.cm.gray)

    # plotting box
    for boxes in foundTextAsBoxes_1:
        bboxData = boxes.split(' ')
        # bboxData = foundTextAsBoxes_1[1].split(' ')
        char = bboxData[0]
        bbox = image.shape[0] - int(bboxData[4]), image.shape[0] - int(bboxData[2]), int(bboxData[1]), int(bboxData[3])

        top, bottom, left, right = bbox
        ax.plot((left, right), (top, top), c='r')
        ax.plot((left, right), (bottom, bottom), c='r')
        ax.plot((left, left), (top, bottom), c='r')
        ax.plot((right, right), (top, bottom), c='r')
        ax.text(left + int((right - left) / 2), (top - 2), char)

    plt.show()


def main():
    # Detection Variables
    correctDetections = []
    incorrectDetections = []

    Directories = []

    # Initialising Tesseract
    pyt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    if TEST_DIR:
        for Directory in TESTING_DIRS:
            Directories.append(os.path.join(TESTING_DATA, Directory))
    else:
        Directories.append(TESTING_DATA)

    for dir in Directories:
        # Detection Variables
        cdetections = []
        idetections = []
        # Retrieving image names
        fileNames, GTFiles = getFileNames(dir)

        for file in fileNames:
            # Importing Image
            image_1 = importImage(dir + '\\' + file)

            # Get Ground Truth
            groundTruth = getGroundTruth(os.path.join(dir, (splitext(file)[0] + '.gt.txt')))

            # Performing OCR With Tesseract
            foundTextAsString_1 = pyt.image_to_string(image_1, lang=LANG_MODEL1, config=CONFIG1)
            foundTextAsString_1 = foundTextAsString_1.split('\n')

            # Obtain Results
            if foundTextAsString_1[0] == groundTruth:
                cdetections.append(file)
            else:
                incorrectDetection = 'Incorrect Detection: ' + file + ' | Detected / instead of:' + '\n' + str(
                    foundTextAsString_1[0]) + ' \n ' + groundTruth + ' | ' + os.path.split(dir)[1]
                idetections.append(incorrectDetection)
        incorrectDetections.append(idetections)
        correctDetections.append(cdetections)
        # Output Result Data
        percentageAccuracy = (len(cdetections) / len(fileNames)) * 100
        print('Model: ' + LANG_MODEL1 + ' | Testing Data: ' + os.path.split(dir)[1] + '\n')
        print('Successfully Detected: ' + str(len(cdetections)) + '/' + str(len(fileNames)) + ' (' + str(
            round(percentageAccuracy, 2)) + '%)')
        print(str(len(idetections)) + ' Incorrect Detections\n\n')

    return incorrectDetections, correctDetections


incorrectDetections, correctDetections = main()
