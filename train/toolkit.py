import string, random
from PIL import Image
import cv2, imutils
import numpy as np
import exifread

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def make_black_bg(dimensions):
    width, height = dimensions[0], dimensions[1]
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image[:width] = (0, 0, 0)  # (B, G, R)
    pi = Image.fromarray(blank_image)  # convert back to PIL image format
    return pi

def resize(img, size):
    """
    Resizes the resolution of the input image
    :param img:  input image data
    :param size: new size tuple (w,h)
    :return: image data will be resized to new size
    """
    r_channel, g_channel, b_channel, alpha_channel = cv2.split(img)
    img_RGBA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    res = cv2.resize(img_RGBA, size, interpolation=cv2.INTER_CUBIC)
    pi = Image.fromarray(res)  # convert back to PIL image format
    return pi


def make_bg_transparent(img_data, black=False):
    """
    turns white/black background into transparent
    :param img_data: PIL Image data
    :param black: is the background black? default false
    :return: image data with background subtracted
    """
    img = img_data.convert("RGBA")
    datas = img.getdata()

    newData = []

    pixel_value = 0 if black else 255

    for item in datas:
        if item[0] == pixel_value and item[1] == pixel_value and item[2] == pixel_value:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)

    return img

def modify_foreground(img_data, exif_data, new_size):
    """
    performs image transformations (resize/darken) on img_data
    darkening of image depends on time of the day (thru exif data)
    :param img_data: PIL Image data
    :param exif_data: image EXIF data
    :param new_size: size tuple (w,h). image_data will be of dimensions new_size after resizing
    :return: modified image with dimensions new_size and darkened depending on the time of the day
    """
    cv2img = np.array(img_data) #from PIL to CV2
    resized_img = resize(cv2img, new_size)
    black_bg = make_black_bg(new_size) #black background for darkening purposes

    hour = get_hours(exif_data)

    # image gets darkened if its taken between 5pm-5am

    if (hour > 5 and hour <= 7) or (hour >= 18 and hour < 22):
        darkened_resized_img = resized_img.point(lambda p: p * .6)
    elif (hour >= 22 or hour <= 5):
        darkened_resized_img = resized_img.point(lambda p: p * .4)
    else:
        return resized_img #no darkening required if hour not within bounds above

    black_bg.paste(darkened_resized_img, (0,0), darkened_resized_img)

    final_img = make_bg_transparent(black_bg, True)

    return final_img

def get_hours(exif_data):
    """
    :param exif_data: image exif data parsed using exifread
    :return: hour (0-23) of the day in which the image was taken
    """
    for tag in exif_data.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):  # these are not printable
            dt_value = str(exif_data['Image DateTime']).split()
    time = dt_value[1].split(':')
    hour = int(time[0])

    return hour

def tighten_images(img_data):
    """crops images tightly around the biggest contour
    img_data: image loaded through cv2"""
    gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV )[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    max = (cv2.contourArea(cnts[0]), cnts[0])
    for c in cnts:
        curr = cv2.contourArea(c)
        if curr > max[0 ]:
            max = (curr, c)


    [x, y, w, h] = cv2.boundingRect(max[1])
    crop_img = img_data[y:y + h, x:x + w]

    return crop_img

def generate_label(bg_size, obj_class, box):
    """
    :param bg_size: size tuple of the foreground (w,h)
    :param obj_class: 0-3 object class, index in header of create_images_and_labels.py
    :param box: list -> [left, right, bottom, top]
    :return: string to write for label in YOLO v2 format:
    [category number] [object center in X] [object center in Y] [object width in X] [object width in Y]
    """
    dw = 1./bg_size[0]
    dh = 1./bg_size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh

    strToWrite = "{} {} {} {} {}".format(obj_class, x, y, w, h)

    return strToWrite