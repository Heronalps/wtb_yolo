from PIL import Image
import sys, os

def crop_image(input_image, output_image, (x1, y1, x2, y2)):
    '''(x1,y1) and (x2,y2) must be opposite points of the desired box to be cropped
    WARNING!!!! THIS ERASES METADATA!!!!'''
    input_img = Image.open(input_image)
    box = (x1, y1, x2, y2)
    output_img = input_img.crop(box)
    output_img.save(output_image)

if __name__ == '__main__':
    CAM_CONFIG = [(0,35,1920,1010)]

    config = int(sys.argv[1])
    bg_dir = sys.argv[2]
    out_dir = sys.argv[3]

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for image in os.listdir(bg_dir):
        image_path = bg_dir + '/' + image
        out_path = out_dir + '/' + image
        crop_image(image_path, out_path, CAM_CONFIG[config - 1])

    print "Success"