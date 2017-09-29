import sys, os
from PIL import Image
import urllib, cStringIO
from toolkit import make_bg_transparent

def download_and_subtract(image_link):
    """
    :param image_link: Link to image with white background
    :return: image data with subtracted background)
    """
    print image_link
    file = cStringIO.StringIO(urllib.urlopen(image_link).read())
    img = Image.open(file)
    return make_bg_transparent(img)

def parse_txt(txt_input):
    """
    :param txt_input: .txt file with its filename as the category
    and image links for every line
    :return: [imagedata1, imagedata2,...]
    """
    f = open(txt_input, 'r')
    content = []
    for line in f:
        content.append(download_and_subtract(line[:-1]))
    return content


if __name__ == '__main__':
    txt_file = sys.argv[1]
    out_path = os.path.basename(txt_file)[:-4] #get rid of .txt
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    txt_content = parse_txt(txt_file)
    count = 1
    for img_data in txt_content:
        img_data.save("{}/{}{}.png".format(out_path, out_path, count), "PNG")
        count += 1