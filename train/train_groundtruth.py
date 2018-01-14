"""

TRAIN WITH GROUNDTRUTH DATA
INPUT: gt_data.json
OUTPUT: data has been parsed and ready to train in train_gt/

"""

import os, sys
from PIL import Image
import urllib, cStringIO
from toolkit import generate_label
import json

def parse(gt_data, out_dir):
    for key in gt_data:
        fname = key[key.index(".edu/")+ 5:].replace("%20", "_")
        file = cStringIO.StringIO(urllib.urlopen(key).read())
        img = Image.open(file)
        w,h = img.size
        if len(gt_data[key]) == 0:
            continue

        labels = []
        for data in gt_data[key]:
            l = data['x']
            r = data['width'] + l
            b = data['y']
            t = data['height'] + b
            box = [l, r, b, t] #[left, right, bottom, top]

            strToWrite = generate_label((w,h), 0, box)
            labels.append(strToWrite)

        img.save(out_dir + '/' + fname)

        f = open(out_dir + '/' + fname[:-4] + '.txt', 'w')
        for l in labels:
            f.write(l + '\n')

        f.close()

        print fname, labels


if __name__ == '__main__':
    data_json = sys.argv[1]
    out_dir = sys.argv[2]

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    j =  json.load(open(data_json, "r"))
    parse(j, out_dir)
    print "Success"