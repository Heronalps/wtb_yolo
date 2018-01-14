import os, sys

def generate_links(ip, html_directory):
    """
    :param html_directory: apache html directory (usually under /var/www/html/ in linux)
    :return: list of link postfixes for each image
    """
    suffixes = []
    for file in os.listdir(html_directory):
        link = file.replace(" ", "%20")
        suffixes.append("{}/{}".format(ip, link))
    return suffixes

if __name__ == '__main__':
    img_dir = sys.argv[1]
    ip = sys.argv[2]

    links = generate_links(img_dir, ip)
    f = open("outlinks.csv", 'w')
    f.write("image_url\n")
    for item in links:
        f.write(item + '\n')