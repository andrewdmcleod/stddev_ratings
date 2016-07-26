from collections import Counter
import numpy as np
import pprint
import json

with open("best_of_2014.json") as json_file:
    json_data = json.load(json_file)
    json_data.sort()
    for item in json_data:
        a = item['page'].split()
        item['page'] = a[1]
#    pprint.pprint(json_data)
    #for item in json_data:
        #print item
        #for key, value in item.items():
        #    print key, value
    newlist = sorted(json_data, reverse=True, key=lambda k: (k['title'], int(k['page'])))
#    boblist = max(json_data, key=lambda k: (k['title'], int(k['page'])))
    title = ''
    std_array = [] 
    print type(json_data)
    print type(newlist)
    for item in newlist:
        for k, v in item.iteritems():
            if k == 'title':
                if v != title:
                    title = v
                    std_array.append(item)
#                    print item
    print type(std_array)
    std_list = sorted(std_array, reverse=True, key=lambda k: float(k['std_dev']))
    for item in std_list:
        print item
