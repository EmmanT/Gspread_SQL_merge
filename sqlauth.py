import json

def sqlauth():
    json_key = json.load(open('yatapka.json'))
    return json_key['vhost'], json_key['vuser'], json_key['vpass'], json_key['vdb'], json_key['query'], json_key['listcolnames']