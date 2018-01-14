import json, sys

def parse(json_fpath):
    f = open(json_fpath, 'r')
    parsed_data = {}
    for line in f:
        j = json.loads(line)
        image_bbox = j['results']['annotation']['bagg_0.4']
        image_bbox = eval(image_bbox)
        if len(image_bbox) == 0:
            image_bbox = {}
        image_url = str(j['data']['image_url'])
        parsed_data[image_url] = image_bbox

    return parsed_data

if __name__ == '__main__':
    json_file = sys.argv[1]
    data = parse(json_file)
    with open('parsed_' + json_file, 'w') as outfile:
        outfile.write(json.dumps(data, sort_keys=True, indent = 4, separators = (',', ': ')))



