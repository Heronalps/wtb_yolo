from PIL import Image, ImageDraw
import cv2
import numpy as np
import sys

def resize(img, size):
    """
    Resizes the resolution of the input image
    :param img:  input image data
    :param size: new size tuple (w,h)
    :return: image data will be resized to new size
    """
    img = cv2.imread("bear/bear2.png", -1)
    b_channel, g_channel, r_channel, alpha_channel = cv2.split(img)
    img_RGBA = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))

    res = cv2.resize(img_RGBA, size, interpolation=cv2.INTER_CUBIC)
    pi = Image.fromarray(res)  # convert back to PIL image format
    return pi

def get_bbox(location, size):
    """
    :param location: (x,y) tuple containing the location of the top-left corner of the foreground
    :param size: tuple (w,h) containing size of the foreground
    :return: 4 values for bbox: left, bottom, right, top
    """
    left = location[0] # left = x-coord
    top = location[1] # top = y-coord
    bottom = top + size[1] # bottom = top - height
    right = left + size[0] # right = left + width

    return left, bottom, right, top

def create_montague(background, foreground, location, resize_factor=10, out_dir="out"):
    """
    creates a synthetic image of an animal in a empty background along with a bounding box

    :param background: path to backround image
    :param foreground: path to foreground image
    :param location: (x,y) coordinates of where the top-left corner of the image is placed
    :param resize_factor: do you want to resize the foreground? default is 10
    :param out_dir: where images and .txt containing bounding boxes are saved, default is "out/"

    :return: montague + .txt file containing bbox is saved under out_dir
    """

    background = Image.open(background) # operations are done through PIL
    foreground = cv2.imread(foreground) #resizing is done through cv2
    h, w = foreground.shape[:2]
    w /= 10
    h /= 10

    resized_foreground = resize(foreground, (w,h))
    left, bottom, right, top = get_bbox(location, (w,h))
    print left, bottom, right, top
    background.paste(resized_foreground, location, resized_foreground)
    ImageDraw.Draw(background).rectangle(([left, top, right,bottom]), outline='red')
    background.show()

create_montague("IMG_0052.JPG", "bear/bear2.png", (245,553))