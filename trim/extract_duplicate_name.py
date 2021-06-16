import json
import pprint
import collections

with open('./jfdb_after2003.jsonlines', mode='r') as f_r:
    name_id = {}
    for row in f_r.readlines():
        for cast in json.loads(row)['出演者']:
            if cast['id'] not in name_id:
                name_id[cast['id']] = cast['名前']

    pprint.pprint([k for k, v in collections.Counter([name_id[id]
                                                      for id in name_id.keys()]).items() if v > 1])

    # for id in name_id.keys():
    #     if name_id[id] == 'ムロツヨシ':
    #         print(name_id[id], id)
