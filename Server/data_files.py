import json

def create_data_file():
    files = {'files': {}}

    with open('data.json', 'w') as file:
        json.dump(files, file)


def open_data_file():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

def add_file(name, size, blocks):

    data = open_data_file()

    data['files'][name] = {
        "size": size,
        "blocks": blocks,
        "nodes": {}
    }

    with open('data.json', 'w') as file:
        json.dump(data, file)


def get_files():
    data = open_data_file()['files']
    files = list(data.keys())

    return files

def add_node(name, block, node):
    data = open_data_file()

    if block in data['files'][name]['nodes']:
        data['files'][name]['nodes'][block].append(node)
    else:
        data['files'][name]['nodes'][block] = [node]

    with open('data.json', 'w') as file:
        json.dump(data, file)

def get_nodes(name):
    data = open_data_file()

    return data['files'][name]['nodes']
