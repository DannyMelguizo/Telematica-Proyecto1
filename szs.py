import json

data = {"files": {"file.mp3": {"size": 4376748, "blocks": 17, "nodes": {"1": ["54.167.36.42"], "2": ["204.236.214.107"], "3": ["54.167.36.42"], "4": ["204.236.214.107"]}}}}

node = data["files"]["file.mp3"]["nodes"]


keys = json.dumps(list(node.keys()))
values = json.dumps(list(node.values()))

bkeys = bytes(keys, 'utf-8')
bvalues = bytes(values, 'utf-8')

print(bkeys)
print(bvalues)

