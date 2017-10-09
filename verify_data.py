import os, sys, cv2

def verify(data_dir):
    """
    verifies that each .jpg has a corresponding .txt file
    :param data_dir: directory with all the jpg + txt files
    :return: if a file is missing its jpg/txt counterpart, such file(s) has been removed
    """
    dir_files = os.listdir(data_dir)
    for file in dir_files:
        filename = file[:-4]
        filename_jpg = filename + '.jpg'
        filename_txt = filename + '.txt'
        if filename_jpg not in dir_files or filename_txt not in dir_files:
            print file
            os.remove(data_dir+'/'+file)

def convert_bbox(yolo_bbox):
    """
    converts yolo format:
    [object center in X] [object center in Y] [object width in X] [object width in Y]
    to:
    [bounding box left X] [bounding box top Y] [bounding box right X] [bounding box bottom Y]
    :param yolo_bbox: bounding box in yolo format
    :return: bounding box in left,top,right,bottom format
    """
    x, y, w, h = yolo_bbox[0], yolo_bbox[1], yolo_bbox[2], yolo_bbox[3]
    W = (w * 1920) / 2
    H = (h * 1090) / 2
    right = x * 1920 + (w * 1920) / 2
    top = y * 1090 - (h * 1090) / 2
    left = x * 1920 - (w * 1920) / 2
    bottom = y * 1090 + (h * 1090) / 2
    print left, top, right, bottom
    return left, top, right, bottom

def check_bbox(img_data, yolo_bbox):
    """
    draws the bounding box on the image for verification
    :param img_data: cv2-loaded image data
    :param yolo_bbox: bounding box in yolov2 format
    [object center in X] [object center in Y] [object width in X] [object width in Y]
    :return: None
    """
    left, top, right, bottom = convert_bbox(yolo_bbox)
    cv2.rectangle(img_data, (int(left), int(top)), (int(right), int(bottom)), (255,255,255))
    window = cv2.namedWindow("Final", 0)
    window = cv2.resizeWindow(window, 500, 500)
    cv2.imshow(window, img)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    data_dir = "out/bear"
    for jpg in os.listdir(data_dir):
        if ".jpg" in jpg:
            fpath = data_dir + '/' + jpg
            img = cv2.imread(fpath)
            txt = fpath[:-4] + '.txt'
            bbox = open(txt, 'r')
            bbox = bbox.readline()
            bbox = bbox.split(" ")[1:]
            bbox = map(float, bbox)
            check_bbox(img, bbox)
            print bbox, img.shape[:2]