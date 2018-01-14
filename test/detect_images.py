import sys, os

CLASSES = ["bear"]

class Box:
    def __init__(self, left, right, top, bottom):
        """
        :param left: left plane of the bbox
        :param right: right plane of the bbox
        :param top:  top plane of the bbox
        :param bottom:  bottom plane of the bbox
        """
        self.left = left
        self.right = right
        self.top = top
        self. bottom = bottom

class Object:
    def __init__(self, objectClass, bbox):
        """
        :param objectClass: index number of the object class
        :param bbox
        """
        self.objectClass = objectClass
        self.bbox = bbox

class Image:
    def __init__(self, object_list, filename):
        self.objects = object_list
        self.imageName = filename


def detect(image, weight):
    """
    Runs YOLOv2 on given image
    :param image: path of image to be detected
    :return: list of Image object each containing all objects detected along with their bounding boxes
    """
    os.system("./darknet detector test cfg/obj.data cfg/yolo-obj.cfg {} {} > out.txt".format(image, weight))
    f = open("out.txt", 'r')
    lines = f.readlines()
    if lines > 2:
        detections = lines[3]
    else:
        return None

    detections = detections.split(" ")
    detections = detections[:-1]
    fname = os.path.basename(image)[:4]

    objectList = []
    for bbox in detections:
        bbox = bbox.split(",")
        for b in bbox:
            objClass = b[0]
            left = b[1]
            right = b[2]
            top = b[3]
            bottom = b[4]
            box = Box(left, right, left, bottom)
            obj = Object(objClass, box)
            objectList.append(obj)

    img = Image(objectList, fname)
    return img

def parse(img_dir, weight):
    """
    Detects all images in img_dir
    :param img_dir: directory with all images to be detected
    :return: a list of Image objects with the detected objects and respective bounding boxes
    """
    images = []
    for image in os.listdir(img_dir):
        image_path = img_dir + '/' + image
        img = detect(image_path, weight)
        images.append(img)

    return images

def parse(imageList):
    for image in imageList:
        strToWrite = ''
        for obj in image.objects:
            imageName = image.imageName
            objClass = obj.objectClass
            left = obj.bbox.left
            right = obj.bbox.right
            bottom = obj.bbox.bottom
            top = obj.bbox.top
            if image.objects.index(obj) == image.objects[:-1]:
                strToWrite += "{}\t{} {} {} {} {}\n"
                #TODO: Finish this

if __name__ == '__main__':
    img_dir = sys.argv[1]
    weight = sys.argv[2]

    outdir = "out"

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    for image in os.listdir(img_dir):
        image_path = img_dir + '/' + image
        img = detect(image_path, weight)
        os.rename("prediction.png", outdir + '/' + image)
        os.rename('out.txt', outdir + '/' + image[:-4] + '.txt')