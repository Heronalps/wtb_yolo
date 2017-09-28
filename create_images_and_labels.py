import cv2
from PIL import Image, ImageDraw
import numpy as np
import sys, os, random
import string

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def resize(img, size):
    """
    Resizes the resolution of the input image
    :param img:  input image data
    :param size: new size tuple (w,h)
    :return: image data will be resized to new size
    """
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

def create_montague(background_data, foreground_data, location, resize_factor=10, out_dir="out"):
    """
    creates a synthetic image of an animal in a empty background along with a bounding box

    :param background: backround image data - must be loaded though PIL
    :param foreground: foreground image data - must be loaded through cv2
    :param location: (x,y) coordinates of where the top-left corner of the image is placed
    :param resize_factor: do you want to resize the foreground? default is 10
    :param out_dir: where images and .txt containing bounding boxes are saved, default is "out/"

    :return: montague + .txt file containing bbox is saved under out_dir
    """

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    h, w = foreground_data.shape[:2]
    w /= resize_factor
    h /= resize_factor


    resized_foreground = resize(foreground_data, (w,h))
    left, bottom, right, top = get_bbox(location, (w,h))
    print left, bottom, right, top
    background_data.paste(resized_foreground, location, resized_foreground)
    background_data.save(out_dir + '/' + id_generator() + '.jpg')

def generate_locations(background_size):
    """
    Generates locations where foregrounds can be placed in
    :param background: background image size tuple (w, h)
    :return:
    """
    bg_w = background_size[0]
    bg_h = background_size[1]
    locations_list = []
    for x in range(1, bg_w, (bg_w / 10)):
        bg_middle1 = bg_h - (bg_h / 4)
        bg_middle2 = bg_h - (bg_h / 3)
        bg_middle3 = bg_h - (bg_h / 2)
        locations = [(x, bg_middle1), (x,bg_middle2), (x,bg_middle3)]
        locations_list += locations

    random.shuffle(locations_list)

    return locations_list[:10]

def get_resize_factor(foreground_size):
    """
    :param foreground_size: foreground image size tuple (w, h)
    :return: optimal scaling factor for given foreground
    """
    #TODO: finish this
    dim = foreground_size[0]
    count = 0
    while dim > 500:
        count +=1
        dim *= 2/3.0
    print dim, count


def create_montage_dir(background_dir, foreground_dir):
    """
    creates montagues for every background and foreground
    :param background_dir: directory with empty images
    :param foreground_dir: directory with cropped animals
    :return:
    """


    for bg_image in os.listdir(background_dir):
        bg_image = background_dir + '/' + bg_image
        background = Image.open(bg_image)  # operations are done through PIL
        out_dir = "out/" + os.path.basename(foreground_dir)
        for fg_image in os.listdir(foreground_dir):
            fg_image = foreground_dir + '/' + fg_image
            print bg_image, fg_image
            foreground = cv2.imread(fg_image, -1)  # resizing is done through cv2
            foreground_flipped = cv2.flip(foreground, 1)
            locations = generate_locations((background.width, background.height))
            locations_flipped = generate_locations((background.width, background.height))
            for img_location in locations:
                background_copy = background.copy()
                size = random.randint(7, 9) #scaling factor foreground size
                create_montague(background_copy, foreground, img_location, size, out_dir)
            for img_location_flipped in locations_flipped:
                background_copy = background.copy()
                size = random.randint(7, 9)  # scaling factor foreground size
                create_montague(background_copy, foreground_flipped, img_location_flipped, size, out_dir)


create_montage_dir("background", "bear")

