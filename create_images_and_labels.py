import os
from toolkit import *

classes = ["bear", "deer", "coyote"]

def generate_label(bg_size, obj_class, box):
    """
    :param bg_size: size tuple of the foreground (w,h)
    :param obj_class: 0-3 object class, index in header
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

def get_bbox(location, size):
    """
    :param location: (x,y) tuple containing the location of the top-left corner of the foreground
    :param size: tuple (w,h) containing size of the foreground
    :return: 4 values for bbox: left, top, right, bottom
    """
    left = location[0] # left = x-coord
    top = location[1] # top = y-coord
    bottom = top + size[1] # bottom = top - height
    right = left + size[0] # right = left + width

    return left, top, right, bottom

def create_montague(background_data, foreground_data, exif, location, resize_factor=10, out_dir="out"):
    """
    creates a synthetic image of an animal in a empty background along with a bounding box

    :param background: backround image data - must be loaded though PIL
    :param foreground: foreground image data - must be loaded through cv2
    :param location: (x,y) coordinates of where the top-left corner of the image is placed
    :param resize_factor: do you want to resize the foreground? default is 10
    :param out_dir: where images and .txt containing bounding boxes are saved, default is "out/"

    :return: None, saves montague image file + .txt file containing bbox under out_dir
    """

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    category = os.path.basename(out_dir) # the name of the output folder should be the category name

    h, w = foreground_data.shape[:2]
    w /= resize_factor
    h /= resize_factor


    modified_foreground = modify_foreground(foreground_data, exif ,(w,h))
    left, top, right, bottom = get_bbox(location, (w,h))
    print left, top, right, bottom
    background_data.paste(modified_foreground, location, modified_foreground)
    generated_name = out_dir + '/' + id_generator()
    background_data.save(generated_name + '.jpg') #save under random name

    box = [left, right, top, bottom] # different order needed for generate_label function

    strToWrite = generate_label((background_data.width, background_data.height), classes.index(category), box)

    f = open(generated_name + '.txt', 'w')
    f.write(strToWrite)
    f.close()



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


def create_montague_dir(background_dir, foreground_dir):
    """
    creates montagues for every background and foreground
    :param background_dir: directory with empty images
    :param foreground_dir: directory with cropped animals
    :return:
    """
    for bg_image in os.listdir(background_dir):
        bg_image = background_dir + '/' + bg_image
        background = Image.open(bg_image)  # operations are done through PIL
        f = open(bg_image)
        exif = exifread.process_file(f)
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
                create_montague(background_copy, foreground, exif, img_location, size, out_dir)
            for img_location_flipped in locations_flipped:
                background_copy = background.copy()
                size = random.randint(7, 9)  # scaling factor foreground size
                create_montague(background_copy, foreground_flipped, exif, img_location_flipped, size, out_dir)

create_montague_dir("background", "bear")